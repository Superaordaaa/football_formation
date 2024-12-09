import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# List of common football formations
formations_dict = {
    "4-4-2": [4, 4, 2],
    "4-3-3": [4, 3, 3],
    "3-5-2": [3, 5, 2],
    "4-2-3-1": [4, 2, 3, 1],
    "5-3-2": [5, 3, 2],
    "3-4-3": [3, 4, 3]
}

# Function to draw the football field with player positions
def draw_formation_with_coverage(formation_input, player_color='red', player_size=1.5, coverage_radius=10):
    fig, ax = plt.subplots(figsize=(10, 7))

    # Create the field
    field = patches.Rectangle((0, 0), 105, 68, edgecolor="black", facecolor="green", lw=2)
    ax.add_patch(field)

    # Add center line and circle
    plt.plot([52.5, 52.5], [0, 68], color="white", lw=2)
    center_circle = patches.Circle((52.5, 34), 9.15, edgecolor="white", facecolor="none", lw=2)
    ax.add_patch(center_circle)
    plt.plot(52.5, 34, 'wo')

    # Penalty areas
    penalty_area_left = patches.Rectangle((0, 24.5), 16.5, 19, edgecolor="white", facecolor="none", lw=2)
    penalty_area_right = patches.Rectangle((105 - 16.5, 24.5), 16.5, 19, edgecolor="white", facecolor="none", lw=2)
    ax.add_patch(penalty_area_left)
    ax.add_patch(penalty_area_right)

    # Goal areas
    goal_area_left = patches.Rectangle((0, 30.5), 5.5, 7, edgecolor="white", facecolor="none", lw=2)
    goal_area_right = patches.Rectangle((105 - 5.5, 30.5), 5.5, 7, edgecolor="white", facecolor="none", lw=2)
    ax.add_patch(goal_area_left)
    ax.add_patch(goal_area_right)

    # Goals
    goal_left = patches.Rectangle((-2, 30.5), 2, 7, edgecolor="white", facecolor="none", lw=2)
    goal_right = patches.Rectangle((105, 30.5), 2, 7, edgecolor="white", facecolor="none", lw=2)
    ax.add_patch(goal_left)
    ax.add_patch(goal_right)

    # Calculate player positions based on formation input
    x_positions = [10, 30, 50, 70, 90]  # Pre-defined x-axis positions for rows
    y_spacing = 68 / max(formation_input)  # Adjust y-spacing based on the maximum players in a row
    formation_positions = []

    for i, players_in_row in enumerate(formation_input):
        row_x = x_positions[i] if i < len(x_positions) else x_positions[-1]
        start_y = (68 - (players_in_row - 1) * y_spacing) / 2
        for j in range(players_in_row):
            row_y = start_y + j * y_spacing
            formation_positions.append((row_x, row_y))

    # Plot players with coverage radius
    covered_area = 0  # Initialize covered area
    total_area = 105 * 68  # Total field area (full field)

    for x, y in formation_positions:
        coverage = patches.Circle((x, y), coverage_radius, color='blue', alpha=0.1)
        ax.add_patch(coverage)
        player = patches.Circle((x, y), player_size, color=player_color, ec="black", lw=0.5)
        ax.add_patch(player)

        # Calculate area covered by each player (approximated as a circle)
        covered_area += math.pi * coverage_radius ** 2  # Area of circle = π * r²

    # Calculate coverage percentage for the full field
    coverage_percentage = (covered_area / total_area) * 100

    # Display the coverage percentage
    st.write(f"Field Coverage: {coverage_percentage:.2f}%")

    ax.set_xlim(-5, 110)
    ax.set_ylim(-5, 73)
    ax.set_aspect('equal', adjustable='datalim')
    ax.axis('off')  # Turn off the axis
    st.pyplot(fig)

# Streamlit app layout
st.title('Football Formation Visualizer')

# Dropdown to select formation
formation = st.selectbox(
    'Choose a formation:',
    list(formations_dict.keys()),
    index=0
)

# Draw the formation based on the selected option
draw_formation_with_coverage(formations_dict[formation])
