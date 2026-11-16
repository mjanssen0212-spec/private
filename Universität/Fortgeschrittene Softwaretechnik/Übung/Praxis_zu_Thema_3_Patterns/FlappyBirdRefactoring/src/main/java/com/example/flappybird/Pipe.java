package com.example.flappybird;

import java.awt.*;

/**
 * Pipe.java
 * Handles collisions and rendering for pipes
 *
 * @author  Paul Krishnamurthy
 */

public class Pipe {
	private static final int START_X = FlappyBird.WIDTH + 5;
	// Pipe coordinates
	private int x = START_X;
	private int y;

	// Pipe constants
	public static final int WIDTH         = 67;
	public static final int HEIGHT        = 416;
	public static final int PIPE_DISTANCE = 150;          // Horizontal distance between pipes
	public static final int PIPE_SPACING  = HEIGHT + 170; // Vertical distance between pipes
	private static final int SPEED        = -2;

	// If the bird can get a point passing this pipe
	private boolean canAwardPoint = true;

	/**
	 * Moves the pipe
	 */
	public void move () {
		x += SPEED;
	}

	public void render(Renderer renderer, Graphics g) {
		// Draw the top and bottom pipes
		renderer.drawComponent(y <= 0 ? "pipe-top" : "pipe-bottom", x, y, g);

	}

	/**
	 * Checks for bird colliding with pipe
	 *
	 * @param  rectangle     Bird's hitbox
	 * @return        If bird is colliding with the pipe
	 */
	public boolean collide (Rectangle rectangle) {

		// Do not allow bird to jump over pipe
		if (rectangle.x > x && rectangle.y < 0 && canAwardPoint) {
			return true;
		}

		return rectangle.intersects(new Rectangle(x, y, WIDTH, HEIGHT));

	}

	public boolean checkAwardPoint(Rectangle hitbox) {
		if (hitbox.getX() >= x + (double) WIDTH / 2) {
			// Increase score
			if (canAwardPoint) {
				canAwardPoint = false;
				return true;
			}
		}

		return false;
	}

	public void respawnAsTop() {
		x = START_X;
		y = -Math.max((int) (Math.random() * 320) + 30, 140);
		canAwardPoint = true;
	}

	public void respawnAsBottom(int topY) {
		x = START_X;
		y = topY + PIPE_SPACING;
		canAwardPoint = false;
	}

	/**
	 * @return     Pipe's x-coordinate
	 */
	public int getX () {
		return x;
	}

	/**
	 * @return     Pipe's y-coordinate
	 */
	public int getY () {
		return y;
	}




}

