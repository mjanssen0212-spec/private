package com.example.flappybird; /**
 * Sprites.java
 * Cuts up the main sprite sheet
 *
 * @author  Paul Krishnamurthy
 */

import java.awt.image.BufferedImage;
import java.awt.Graphics2D;
import java.io.IOException;
import java.io.File;
import javax.imageio.ImageIO;
import java.util.HashMap;

public class Sprites {

	// Resize factor to match frame size
	private static final double RESIZE_FACTOR = 2.605;

	private static BufferedImage spriteSheet = null;

	// HashMap of texture objects
	private static HashMap<String, Texture> textures = new HashMap<String, Texture>();

	public Sprites () {

		// Try to load sprite sheet, exit program if cannot

		try {
			spriteSheet = ImageIO.read(this.getClass().getResource("/res/img/spriteSheet.png"));
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("Could not load sprite sheet.");
			System.exit(-1); // Exit program if file could not be found
			return;
		}

		// Backgrounds
		putTexture("background1", 0, 0, 144, 256, 0, 0);
		putTexture("background2", 146, 0, 144, 256, 0, 0);

		// Pipes
		putTexture("pipe-top", 56, 323, 26, 160, 0, 0);
		putTexture("pipe-bottom", 84, 323, 26, 160, 0, 0);

		// Birds
		putTexture("yellowBird1", 31, 491, 17, 12, 172, 250);
		putTexture("yellowBird2", 59, 491, 17, 12, 172, 250);
		putTexture("yellowBird3", 3, 491, 17, 12, 172, 250);

		putTexture("blueBird1", 115, 329, 17, 12, 172, 250);
		putTexture("blueBird2", 115, 355, 17, 12, 172, 250);
		putTexture("blueBird3", 87, 491, 17, 12, 172, 250);

		putTexture("redBird1", 115, 407, 17, 12, 172, 250);
		putTexture("redBird2", 115, 433, 17, 12, 172, 250);
		putTexture("redBird3", 115, 381, 17, 12, 172, 250);

		// Buttons
		putTexture("playButton", 354, 118, 52, 29, 34, 448);
		putTexture("leaderboard", 414, 118, 52, 29, 203, 448);
		putTexture("rateButton", 465, 1, 31, 18, 147, 355);
		
		// Helpful / Text
		putTexture("newHighscore", 112, 501, 16, 7, 210, 305);
		putTexture("titleText", 351, 91, 89, 24, 72, 100);
		putTexture("getReadyText", 295, 59, 92, 25, 68, 180);
		putTexture("gameOverText", 395, 59, 96, 21, 62, 100);
		putTexture("instructions", 292, 91, 57, 49, 113, 300);

		// SCORE IMAGES
		
		// Large numbers
		putTexture("score-0", 496, 60, 12, 18, 0, 0);
		putTexture("score-1", 136, 455, 8, 18, 0, 0);
		
		int score = 2;
		for (int i = 292; i < 335; i += 14) {
			putTexture("score-" + score,  i, 160, 12, 18, 0, 0);
			putTexture("score-" + (score + 4), i, 184, 12, 18, 0, 0);
			score++;
		}

		// Mini numbers
		score = 0;
		for (int i = 323; score < 10; i += 9) {
			putTexture("mini-score-" + score, 138, i, 10, 7, 0, 0);
			score ++;
			if (score % 2 == 0) { i += 8; }
		}

		// Medals
		putTexture("bronze", 112, 477, 22, 22, 73, 285);
		putTexture("silver", 112, 453, 22, 22, 73, 285);
		putTexture("gold", 121, 282, 22, 22, 73, 285);
		putTexture("platinum", 121, 258, 22, 22, 73, 285);

		// Other assets
		putTexture("base", 292, 0, 168, 56, 0, 521);
		putTexture("scoreCard", 3, 259, 113, 57, 40, 230);

	}

	private void putTexture(String name, int x, int y, int width, int height, int resizeX, int resizeY) {
    	textures.put(name, new Texture(resize(spriteSheet.getSubimage(x, y, width, height)), resizeX, resizeY));
	}

	/**
	 * Resizes a BufferedImage
	 * 
	 * @param  image     BufferedImage object
	 * @return           New resized image
	 */
	private static BufferedImage resize (BufferedImage image) {

		// New width and height
		int newWidth = (int) (image.getWidth() * RESIZE_FACTOR);
		int newHeight = (int) (image.getHeight() * RESIZE_FACTOR);

		// Create new BufferedImage with updated width and height
	    BufferedImage resizedImage = new BufferedImage(newWidth, newHeight, BufferedImage.TYPE_INT_ARGB);
	    Graphics2D g = resizedImage.createGraphics();
	    g.drawImage(image, 0, 0, newWidth, newHeight, null);
	    g.dispose();

	    return resizedImage;
	}

	/**
	 * Public getter method for Textures HashMap
	 * 
	 * @return     Texture
	 */
	public HashMap<String, Texture> getGameTextures () {
		return textures;
	}

}

