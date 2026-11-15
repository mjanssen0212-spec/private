package com.example.flappybird;

import java.awt.*;

public class Ground {
    private int[] coordinates;
    private Renderer renderer;
    private int baseSpeed;

    public Ground(int[] coordinates, Renderer renderer, int baseSpeed) {
        this.coordinates = coordinates;
        this.renderer = renderer;
        this.baseSpeed = baseSpeed;
    }

    public void move() {
        coordinates[0] = coordinates[0] - baseSpeed < -435 ? 435 : coordinates[0] - baseSpeed;
        coordinates[1] = coordinates[1] - baseSpeed < -435 ? 435 : coordinates[1] - baseSpeed;
    }

    /**
     * Draws a string centered based on given restrictions
     *
     * @param s     String to be drawn
     * @param w     Constraining width
     * @param h     Constraining height
     * @param y     Fixed y-coordiate
     */


    /**
     * Needs to be called differently based on screen
     */
    public void render (Graphics g) {

        // Moving base effect
        renderer.drawComponent("base", coordinates[0], g);
        renderer.drawComponent("base", coordinates[1], g);

    }
}
