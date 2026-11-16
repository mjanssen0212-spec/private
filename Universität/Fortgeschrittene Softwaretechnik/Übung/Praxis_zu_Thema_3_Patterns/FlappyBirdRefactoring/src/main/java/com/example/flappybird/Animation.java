package com.example.flappybird; /**
 * Animation.java
 * Creates animation with array of sprites
 *
 * @author  Paul Krishnamurthy
 */

import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.awt.geom.AffineTransform;

public class Animation {

	// Start at first frame
	private double currentFrame = 0;
	private BufferedImage[] sprites;
	private double speed;

	public Animation(BufferedImage[] sprites, double speed) {
		this.sprites = sprites;
		this.speed = speed;
	}

	/**
	 * Draws the current frame and advances the animation
	 * 
	 * @param x           x-coordinate
	 * @param y           y-coordinate
	 * @param angle       Angle to rotate sprite
	 */
	public void animate (Graphics g, int x, int y, double angle) {
		
		Graphics2D g2d        = (Graphics2D) g;
		AffineTransform trans = g2d.getTransform();
		AffineTransform at    = new AffineTransform();

		// Number of frames
		int count = sprites.length;

		// Rotate the image
		at.rotate(angle, x + 25, y + 25);
		g2d.transform(at);

		// Draw the current rotated frame
		g2d.drawImage(sprites[(int) (Math.round(currentFrame))], x, y, null);

		g2d.setTransform(trans);
		
		// Switch animation frames
        if (currentFrame >= count - 1) {
            currentFrame = 0;
        } else currentFrame += speed;

	}

}

