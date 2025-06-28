/*
 * ChuhaBot C-based Swarm Controller
 * ================================
 * 
 * High-performance C implementation of swarm behaviors for ChuhaBot robots.
 * This controller provides basic flocking behaviors optimized for real-time
 * performance while maintaining compatibility with the enhanced Python framework.
 * 
 * Features:
 * - Separation, Alignment, and Cohesion behaviors
 * - LIDAR-based neighbor detection
 * - Obstacle avoidance
 * - Configurable behavior weights
 * - Real-time performance optimization
 * 
 * Author: Enhanced ChuhaBot Framework
 * Date: June 2025
 */

#include <webots/robot.h>
#include <webots/motor.h>
#include <webots/lidar.h>
#include <webots/display.h>
#include <webots/keyboard.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Constants
#define MAX_NEIGHBORS 32
#define LIDAR_RANGE_COUNT 16
#define DISPLAY_WIDTH 512
#define DISPLAY_HEIGHT 512
#define MAX_SPEED 60.0
#define PI 3.14159265359

// Behavior weights (configurable)
typedef struct {
    double separation;
    double alignment; 
    double cohesion;
    double obstacle_avoidance;
    double wander;
} BehaviorWeights;

// Neighbor structure
typedef struct {
    double x, y;
    double distance;
    double angle;
} Neighbor;

// Robot state
typedef struct {
    char name[64];
    double position[2];
    double velocity[2];
    double heading;
    int neighbor_count;
    Neighbor neighbors[MAX_NEIGHBORS];
    BehaviorWeights weights;
    int step_count;
    double last_force[2];
} RobotState;

// Global variables
static WbDeviceTag robot_device;
static WbDeviceTag left_motor, right_motor;
static WbDeviceTag lidar;
static WbDeviceTag display;
static RobotState robot_state;
static int timestep;

// LIDAR configuration (from original ChuhaBot)
static double RANGES[LIDAR_RANGE_COUNT] = {
    1.13114178, 0.85820043, 0.57785118, 0.43461093,
    0.38639969, 0.31585345, 0.2667459, 0.23062678,
    0.21593061, 0.19141567, 0.17178488, 0.15571462,
    0.14872716, 0.13643947, 0.12597121, 0.11696267
};
static const double EPSILON = 0.6;
static const double DELTA_THETA = 0.1;
static const double DELTA_R = 0.02;

// Utility functions
double clamp(double value, double min, double max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

double normalize_angle(double angle) {
    while (angle > PI) angle -= 2.0 * PI;
    while (angle < -PI) angle += 2.0 * PI;
    return angle;
}

double vector_magnitude(double x, double y) {
    return sqrt(x * x + y * y);
}

void normalize_vector(double *x, double *y) {
    double mag = vector_magnitude(*x, *y);
    if (mag > 0.001) {
        *x /= mag;
        *y /= mag;
    }
}

// Initialize robot hardware and state
void initialize_robot() {
    // Get robot name
    const char *robot_name = wb_robot_get_name();
    strncpy(robot_state.name, robot_name, sizeof(robot_state.name) - 1);
    
    // Initialize motors
    left_motor = wb_robot_get_device("left motor");
    right_motor = wb_robot_get_device("right motor");
    wb_motor_set_position(left_motor, INFINITY);
    wb_motor_set_position(right_motor, INFINITY);
    wb_motor_set_velocity(left_motor, 0.0);
    wb_motor_set_velocity(right_motor, 0.0);
    
    // Initialize LIDAR
    lidar = wb_robot_get_device("lidar");
    wb_lidar_enable(lidar, timestep);
    
    // Initialize display
    display = wb_robot_get_device("extra_display");
    
    // Initialize keyboard
    wb_keyboard_enable(timestep);
    
    // Initialize robot state
    robot_state.position[0] = 0.0;
    robot_state.position[1] = 0.0;
    robot_state.velocity[0] = 0.0;
    robot_state.velocity[1] = 0.0;
    robot_state.heading = 0.0;
    robot_state.neighbor_count = 0;
    robot_state.step_count = 0;
    robot_state.last_force[0] = 0.0;
    robot_state.last_force[1] = 0.0;
    
    // Default behavior weights
    robot_state.weights.separation = 2.0;
    robot_state.weights.alignment = 1.0;
    robot_state.weights.cohesion = 1.5;
    robot_state.weights.obstacle_avoidance = 3.0;
    robot_state.weights.wander = 0.5;
    
    printf("[%s] C-based ChuhaBot controller initialized\n", robot_state.name);
    printf("LIDAR enabled, Motors configured, Display ready\n");
}

// Detect neighbors using LIDAR data
void detect_neighbors() {
    const float *range_image = wb_lidar_get_range_image(lidar);
    if (!range_image) {
        robot_state.neighbor_count = 0;
        return;
    }
    
    int width = wb_lidar_get_horizontal_resolution(lidar);
    robot_state.neighbor_count = 0;
    
    // Process LIDAR data to find potential neighbors
    for (int i = 0; i < width && robot_state.neighbor_count < MAX_NEIGHBORS; i++) {
        double range = range_image[i];
        
        // Filter out invalid or too close/far readings
        if (range > 0.1 && range < 2.0) {
            double angle = (double)i / width * 2.0 * PI - PI;
            double x = range * cos(angle);
            double y = range * sin(angle);
            
            // Simple filtering - only consider readings that could be neighbors
            if (range > 0.3 && range < 1.5) {
                robot_state.neighbors[robot_state.neighbor_count].x = x;
                robot_state.neighbors[robot_state.neighbor_count].y = y;
                robot_state.neighbors[robot_state.neighbor_count].distance = range;
                robot_state.neighbors[robot_state.neighbor_count].angle = angle;
                robot_state.neighbor_count++;
            }
        }
    }
}

// Separation behavior - avoid crowding neighbors
void calculate_separation(double *force_x, double *force_y) {
    *force_x = 0.0;
    *force_y = 0.0;
    
    for (int i = 0; i < robot_state.neighbor_count; i++) {
        Neighbor *neighbor = &robot_state.neighbors[i];
        if (neighbor->distance < 0.8) {  // Separation threshold
            double diff_x = -neighbor->x;  // Point away from neighbor
            double diff_y = -neighbor->y;
            
            // Weight by inverse distance
            double weight = 1.0 / (neighbor->distance + 0.1);
            *force_x += diff_x * weight;
            *force_y += diff_y * weight;
        }
    }
    
    normalize_vector(force_x, force_y);
}

// Alignment behavior - align with neighbors' direction
void calculate_alignment(double *force_x, double *force_y) {
    *force_x = 0.0;
    *force_y = 0.0;
    
    if (robot_state.neighbor_count > 0) {
        // Simple alignment - move toward average neighbor position
        double avg_x = 0.0, avg_y = 0.0;
        for (int i = 0; i < robot_state.neighbor_count; i++) {
            avg_x += robot_state.neighbors[i].x;
            avg_y += robot_state.neighbors[i].y;
        }
        avg_x /= robot_state.neighbor_count;
        avg_y /= robot_state.neighbor_count;
        
        double angle = atan2(avg_y, avg_x);
        *force_x = cos(angle);
        *force_y = sin(angle);
    }
}

// Cohesion behavior - move toward center of neighbors
void calculate_cohesion(double *force_x, double *force_y) {
    *force_x = 0.0;
    *force_y = 0.0;
    
    if (robot_state.neighbor_count > 0) {
        double center_x = 0.0, center_y = 0.0;
        for (int i = 0; i < robot_state.neighbor_count; i++) {
            center_x += robot_state.neighbors[i].x;
            center_y += robot_state.neighbors[i].y;
        }
        center_x /= robot_state.neighbor_count;
        center_y /= robot_state.neighbor_count;
        
        // Only apply cohesion if neighbors are far enough
        double distance_to_center = vector_magnitude(center_x, center_y);
        if (distance_to_center > 0.5) {
            *force_x = center_x;
            *force_y = center_y;
            normalize_vector(force_x, force_y);
        }
    }
}

// Obstacle avoidance behavior
void calculate_obstacle_avoidance(double *force_x, double *force_y) {
    *force_x = 0.0;
    *force_y = 0.0;
    
    // Use LIDAR data to detect close obstacles
    const float *range_image = wb_lidar_get_range_image(lidar);
    if (!range_image) return;
    
    int width = wb_lidar_get_horizontal_resolution(lidar);
    
    for (int i = 0; i < width; i++) {
        double range = range_image[i];
        if (range > 0.05 && range < 0.4) {  // Close obstacle
            double angle = (double)i / width * 2.0 * PI - PI;
            double avoid_x = -cos(angle);  // Point away from obstacle
            double avoid_y = -sin(angle);
            
            // Weight by inverse distance
            double weight = 1.0 / (range + 0.05);
            *force_x += avoid_x * weight;
            *force_y += avoid_y * weight;
        }
    }
    
    normalize_vector(force_x, force_y);
}

// Wander behavior - random exploration
void calculate_wander(double *force_x, double *force_y) {
    static double wander_angle = 0.0;
    
    // Update wander angle with small random changes
    wander_angle += (rand() / (double)RAND_MAX - 0.5) * 0.2;
    wander_angle = normalize_angle(wander_angle);
    
    *force_x = cos(wander_angle);
    *force_y = sin(wander_angle);
}

// Calculate combined swarm behavior forces
void calculate_swarm_forces(double *total_x, double *total_y) {
    double sep_x, sep_y, align_x, align_y, coh_x, coh_y, avoid_x, avoid_y, wander_x, wander_y;
    
    calculate_separation(&sep_x, &sep_y);
    calculate_alignment(&align_x, &align_y);
    calculate_cohesion(&coh_x, &coh_y);
    calculate_obstacle_avoidance(&avoid_x, &avoid_y);
    calculate_wander(&wander_x, &wander_y);
    
    // Combine forces with weights
    *total_x = robot_state.weights.separation * sep_x +
               robot_state.weights.alignment * align_x +
               robot_state.weights.cohesion * coh_x +
               robot_state.weights.obstacle_avoidance * avoid_x +
               robot_state.weights.wander * wander_x;
               
    *total_y = robot_state.weights.separation * sep_y +
               robot_state.weights.alignment * align_y +
               robot_state.weights.cohesion * coh_y +
               robot_state.weights.obstacle_avoidance * avoid_y +
               robot_state.weights.wander * wander_y;
    
    // Store for visualization
    robot_state.last_force[0] = *total_x;
    robot_state.last_force[1] = *total_y;
}

// Convert force vector to motor velocities
void forces_to_motor_velocities(double force_x, double force_y, double *left_vel, double *right_vel) {
    double force_magnitude = vector_magnitude(force_x, force_y);
    double desired_angle = atan2(force_y, force_x);
    
    // Convert to differential drive
    double forward_speed = force_magnitude * MAX_SPEED * 0.5;
    double turning_speed = desired_angle * MAX_SPEED * 0.3;
    
    *left_vel = clamp(forward_speed - turning_speed, -MAX_SPEED, MAX_SPEED);
    *right_vel = clamp(forward_speed + turning_speed, -MAX_SPEED, MAX_SPEED);
}

// Simple visualization on display
void visualize_state() {
    wb_display_set_color(display, 0x000000);
    wb_display_fill_rectangle(display, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
    
    // Draw robot at center
    wb_display_set_color(display, 0xFFFFFF);
    wb_display_fill_oval(display, DISPLAY_WIDTH/2 - 5, DISPLAY_HEIGHT/2 - 5, 10, 10);
    
    // Draw neighbors
    wb_display_set_color(display, 0xFF0000);
    int scale = 200;
    for (int i = 0; i < robot_state.neighbor_count; i++) {
        int x = DISPLAY_WIDTH/2 + (int)(robot_state.neighbors[i].x * scale);
        int y = DISPLAY_HEIGHT/2 + (int)(robot_state.neighbors[i].y * scale);
        if (x >= 0 && x < DISPLAY_WIDTH && y >= 0 && y < DISPLAY_HEIGHT) {
            wb_display_fill_oval(display, x - 3, y - 3, 6, 6);
        }
    }
    
    // Draw force vector
    wb_display_set_color(display, 0x00FF00);
    int force_x = DISPLAY_WIDTH/2 + (int)(robot_state.last_force[0] * 50);
    int force_y = DISPLAY_HEIGHT/2 + (int)(robot_state.last_force[1] * 50);
    wb_display_draw_line(display, DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2, force_x, force_y);
}

// Handle keyboard input for behavior adjustment
void handle_keyboard() {
    int key = wb_keyboard_get_key();
    
    switch (key) {
        case '1':
            robot_state.weights.separation += 0.5;
            printf("[%s] Separation weight: %.1f\n", robot_state.name, robot_state.weights.separation);
            break;
        case '!':
            robot_state.weights.separation = fmax(0.0, robot_state.weights.separation - 0.5);
            printf("[%s] Separation weight: %.1f\n", robot_state.name, robot_state.weights.separation);
            break;
        case '2':
            robot_state.weights.alignment += 0.5;
            printf("[%s] Alignment weight: %.1f\n", robot_state.name, robot_state.weights.alignment);
            break;
        case '@':
            robot_state.weights.alignment = fmax(0.0, robot_state.weights.alignment - 0.5);
            printf("[%s] Alignment weight: %.1f\n", robot_state.name, robot_state.weights.alignment);
            break;
        case '3':
            robot_state.weights.cohesion += 0.5;
            printf("[%s] Cohesion weight: %.1f\n", robot_state.name, robot_state.weights.cohesion);
            break;
        case '#':
            robot_state.weights.cohesion = fmax(0.0, robot_state.weights.cohesion - 0.5);
            printf("[%s] Cohesion weight: %.1f\n", robot_state.name, robot_state.weights.cohesion);
            break;
        case ' ':
            printf("[%s] Reset to default weights\n", robot_state.name);
            robot_state.weights.separation = 2.0;
            robot_state.weights.alignment = 1.0;
            robot_state.weights.cohesion = 1.5;
            robot_state.weights.obstacle_avoidance = 3.0;
            robot_state.weights.wander = 0.5;
            break;
    }
}

// Main control step
void run_step() {
    robot_state.step_count++;
    
    // Handle keyboard input
    handle_keyboard();
    
    // Detect neighbors
    detect_neighbors();
    
    // Calculate swarm behavior forces
    double force_x, force_y;
    calculate_swarm_forces(&force_x, &force_y);
    
    // Convert to motor velocities
    double left_vel, right_vel;
    forces_to_motor_velocities(force_x, force_y, &left_vel, &right_vel);
    
    // Apply motor commands
    wb_motor_set_velocity(left_motor, left_vel);
    wb_motor_set_velocity(right_motor, right_vel);
    
    // Visualize state
    visualize_state();
    
    // Periodic status output
    if (robot_state.step_count % 100 == 0) {
        printf("[%s] Step %d: Neighbors=%d Force=(%.2f,%.2f) Motors=(%.1f,%.1f)\n",
               robot_state.name, robot_state.step_count, robot_state.neighbor_count,
               force_x, force_y, left_vel, right_vel);
    }
}

// Main function
int main() {
    // Initialize Webots
    wb_robot_init();
    timestep = (int)wb_robot_get_basic_time_step();
    
    // Initialize robot
    initialize_robot();
    
    printf("=== ChuhaBot C-based Swarm Controller ===\n");
    printf("Controls:\n");
    printf("  1/! - Increase/Decrease separation weight\n");
    printf("  2/@ - Increase/Decrease alignment weight\n");
    printf("  3/# - Increase/Decrease cohesion weight\n");
    printf("  Space - Reset to default weights\n");
    printf("Starting swarm behavior...\n");
    
    // Main control loop
    while (wb_robot_step(timestep) != -1) {
        run_step();
    }
    
    wb_robot_cleanup();
    return 0;
}
