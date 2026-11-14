package com.example.flappybird; /**
 * GamePanel.java
 * Main game panel
 *
 * @author  Paul Krishnamurthy
 */

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Random;
import java.util.ArrayList;
import java.util.HashMap;
import java.io.InputStream;
import java.io.BufferedInputStream;
import java.awt.image.BufferedImage;
import java.util.Calendar;

public class GamePanel extends JPanel implements KeyListener, MouseListener {

	
	////////////////////
	// Game variables //
	////////////////////
	private GameSession gameSession;

	private Renderer renderer;



	// Textures
	private Sprites sprites;
	public static HashMap<String, Texture> textures;
	
	// Moving base effect
	private static int baseSpeed    = 2;
	private static int[] baseCoords = { 0, 435 };

	// Game states
	final static int MENU = 0;
	final static int GAME = 1;
	private int gameState = MENU;  

	
	public boolean ready = false;                   // If game has loaded
	private boolean inStartGameState = false;       // To show instructions scren
	private Point clickedPoint = new Point(-1, -1); // Store point when player clicks
	private String medal;                           // Medal to be awarded after each game


	public static Audio audio   = new Audio();


	public GamePanel () {


		this.sprites = new Sprites();
		this.textures = sprites.getGameTextures();

		this.renderer = new Renderer(textures);

		this.gameSession = new GameSession(textures);
		restart(); // Reset game variables

		// Input listeners
		addKeyListener(this);
		addMouseListener(this);

	}



	public static void playHitSound () {
		audio.hit();
	}

	/**
	 * To start game after everything has been loaded
	 */
	public void addNotify() {
		super.addNotify();
		requestFocus();
		ready = true;
	}

	/**
	 * Restarts game by resetting game variables
	 */
	public void restart () {

		this.gameSession = new GameSession(textures);

	}

	/**
	 * Checks if point is in rectangle
	 * 
	 * @param      r     Rectangle
	 * @return           Boolean if point collides with rectangle
	 */
	private boolean isTouching (Rectangle r) {
		return r.contains(clickedPoint);
	}

	@Override
	public void paintComponent (Graphics g) {
		super.paintComponent(g);

		Bird gameBird = gameSession.getBird();

		// Set font and color
		g.setFont(renderer.getFlappyFontReal());
		g.setColor(Color.white);

		// Only move screen if bird is alive
		if (gameBird.isAlive()) {

			// Move base
			moveGround(0);
			moveGround(1);

		}

		// Background
		renderer.drawComponent(gameSession.isDarkTheme() ? "background2" : "background1", 0, 0, g);

		// Draw bird
		gameBird.renderBird(g);

		switch (gameState) {

			case MENU:

				drawBase(g);

				drawMenu(g);

				gameBird.menuFloat();

				break;

			case GAME:

				if (gameBird.isAlive()) {

					// Start at instructions state
					if (inStartGameState) {
						startGameScreen(g);

					} else {
						// Start game
						pipeHandler(g);
						gameBird.inGame();
					}

					drawBase(g);

					drawScore(g, gameSession.getScore(), false, 0, 0); // Draw player score

				} else {

					pipeHandler(g);

					drawBase(g);

					// Draw game over assets
					gameOver(g);

				}

				break;
		}

	}

	private void moveGround(int index) {
		baseCoords[index] = baseCoords[index] - baseSpeed < -435 ? 435 : baseCoords[index] - baseSpeed;
	}

	/////////////////////////
	// All drawing methods //
	/////////////////////////

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
	public void drawBase (Graphics g) {

		// Moving base effect
		renderer.drawComponent("base", baseCoords[0], g);
		renderer.drawComponent("base", baseCoords[1], g);

	}

	////////////////
	// Menuscreen //
	////////////////

	private void drawMenu (Graphics g) {

		// Title
		renderer.drawComponent("titleText", g);

		// Buttons
		renderer.drawComponent("playButton", g);
		renderer.drawComponent("leaderboard", g);
		renderer.drawComponent("rateButton", g);

		// Credits :p
		renderer.drawCredits("Created by Paul Krishnamurthy", "www.PaulKr.com", g);
	}



	/////////////////
	// Game screen //
	/////////////////

	public void startGameScreen (Graphics g) {

		// Set bird's new position
		gameSession.getBird().setGameStartPos();

		// Get ready text
		renderer.drawComponent("getReadyText", g);

		// Instructions image
		renderer.drawComponent("instructions", g);

	}

	/**
	 * Aligns and draws score using image textures
	 * 
	 * @param mini     Boolean for drawing small or large numbers
	 * @param x        X-coordinate to draw for mini numbers
	 */
	public void drawScore (Graphics g, int drawNum, boolean mini, int x, int y) {
	
		// Char array of digits
		char[] digits = ("" + drawNum).toCharArray();
		
		int digitCount = digits.length;

		// Calculate width for numeric textures
		int takeUp = 0;
		for (char digit : digits) {

			// Size to add varies based on texture
			takeUp += digitSize(digit, mini);
		}

		// Calculate x-coordinate
		int drawScoreX = mini ? (x - takeUp) : (FlappyBird.WIDTH / 2 - takeUp / 2);

		// Draw every digit
		for (int i = 0; i < digitCount; i++) {
			renderer.drawComponent((mini ? "mini-score-" : "score-") + digits[i], drawScoreX, mini ? y : 60, g);
			
			// Size to add varies based on texture
			drawScoreX += digitSize(digits[i], mini);
		}

	}

	private int digitSize(char digit, boolean mini) {
		if (mini) {
			return 18;
		} else {
			return digit == '1' ? 25 : 35;
		}
	}

	/**
	 * Moves and repositions pipes
	 */
	public void pipeHandler (Graphics g) {
		int pipeDist = gameSession.getPipeDistTracker();
		Bird gameBird = gameSession.getBird();
		ArrayList<Pipe> pipes = (ArrayList<Pipe>) gameSession.getPipes();

		// Decrease distance between pipes
		if (gameBird.isAlive()) {
			gameSession.reducePipeDist();
		}

		// Initialize pipes as null
		Pipe topPipe = null;
		Pipe bottomPipe = null;

		// If there is no distance,
		// a new pipe is needed
		if (pipeDist < 0) {

			// Reset distance
			gameSession.setPipeDistTracker(Pipe.PIPE_DISTANCE);

			for (Pipe p : pipes) {

				// If pipe is out of screen
				if (p.getX() < 0) {
					if (topPipe == null) { 
						topPipe = p;
					}
					else if (bottomPipe == null) {
						bottomPipe = p; 
					}
					topPipe.setCanAwardPoint(true);
				}
			}

			// Move and handle initial creation of top and bottom pipes

			topPipe = addOrReset(topPipe, "top");

			bottomPipe = addOrReset(bottomPipe, "bottom");
			bottomPipe.setCanAwardPoint(false);

			// Set y-coordinate of bottom pipe based on 
			// y-coordinate of top pipe
			bottomPipe.setY(topPipe.getY() + Pipe.PIPE_SPACING);

		}

		// Move and draw each pipe

		for (Pipe p : pipes) {

			// Move the pipe
			if (gameBird.isAlive()) {
				p.move();
			}

			// Draw the top and bottom pipes
			renderer.drawComponent(p.getY() <= 0 ? "pipe-top" : "pipe-bottom", p.getX(), p.getY(), g);

			// Check if bird hits pipes
			if (gameBird.isAlive()) {
				if (p.collide(
					gameBird.getHitbox()
				)) {
					// Kill bird and play sound
					gameBird.kill();
					audio.hit();
				} else {

					// Checks if bird passes a pipe
					if (gameBird.getX() >= p.getX() + p.WIDTH / 2) {

						// Increase score and play sound
						if (p.getCanAwardPoint()) {
							audio.point();
							gameSession.addScore();
							p.setCanAwardPoint(false);
						}
					}
				}
			}
		}
	}

	private Pipe addOrReset(Pipe p, String pipeType) {
		if (p == null) {
			p = new Pipe(pipeType);
			gameSession.addPipe(p);
		} else {
			p.reset();
		}

		return p;
	}

	public void gameOver (Graphics g) {

		int score = gameSession.getScore();
		Highscore highscore = gameSession.getHighscore();
		// Game over text
		renderer.drawComponent("gameOverText", g);

		// Scorecard
		renderer.drawComponent("scoreCard", g);

		// New highscore image
		if (gameSession.isNewHighscore()) {
			renderer.drawComponent("newHighscore", g);
		}

		// Draw mini fonts for current and best scores
		drawScore(g, score, true, 303, 276);
		drawScore(g, highscore.bestScore(), true, 303, 330);

		// Handle highscore
		if (score > highscore.bestScore()) {

			// New best score
			gameSession.setNewHighscore(true);
			highscore.setNewBest(score); // Set in data file
		}

		// Medal
		if (score >= 10) { medal = "bronze"; }
		if (score >= 20) { medal = "silver"; }
		if (score >= 30) { medal = "gold"; }
		if (score >= 40) { medal = "platinum"; }

		// Only award a medal if they deserve it
		if (score > 9) {
			renderer.drawComponent(medal, g);
		}

		// Buttons
		renderer.drawComponent("playButton", g);
		renderer.drawComponent("leaderboard", g);

	}


	//////////////////////
	// Keyboard actions //
	//////////////////////

	public void keyTyped (KeyEvent e) {}
	public void keyReleased (KeyEvent e) {}

	public void keyPressed (KeyEvent e) {

		int keyCode = e.getKeyCode();

		if (gameState == MENU) {

			// Start game on 'enter' key
			if (keyCode == KeyEvent.VK_ENTER) {
				startGame();
			}

		} else if (gameState == GAME && gameSession.getBird().isAlive()) {

			if (keyCode == KeyEvent.VK_SPACE) {

				// Exit instructions state
				inStartGameState = false;

				// Jump and play audio even if in instructions state
				flap();
			}
		}
	}

	///////////////////
	// Mouse actions //
	///////////////////

	public void mouseExited (MouseEvent e) {}
	public void mouseEntered (MouseEvent e) {}
	public void mouseReleased (MouseEvent e) {}
	public void mouseClicked (MouseEvent e) {}

	public void mousePressed (MouseEvent e) {
		Bird gameBird = gameSession.getBird();

		// Save clicked point
		clickedPoint = e.getPoint();

		if (gameState == MENU) {

			if (isTouching(getTextureRect("playButton"))) {
				startGame();

			} else if (isTouching(getTextureRect("leaderboard"))) {

				// Dummy message
				showErrorMessage();
			}

			if (gameBird.isAlive()) {

				if (isTouching(getTextureRect("rateButton"))) {
					Helper.openURL("http://paulkr.com"); // Open website
				}

			}

		} else if (gameState == GAME) {

			if (gameBird.isAlive()) {

				// Allow jump with clicks
				inStartGameState = false;

				// Jump and play sound
				flap();

			} else {

				// On game over screen, allow restart and leaderboard buttons
				if (isTouching(getTextureRect("playButton"))) {
					startGame();
					restart();
					gameBird.setGameStartPos();

				} else if (isTouching(getTextureRect("leaderboard"))) {

					// Dummy message
					showErrorMessage();
				}

			}
			
		}

	}

	private void startGame() {
		gameState = GAME;
		inStartGameState = true;
	}

	private void flap() {
		gameSession.getBird().jump();
		audio.jump();
	}

	public Rectangle getTextureRect(String textureName) {
		return textures.get(textureName).getRect();
	}

	public void showErrorMessage() {
		JOptionPane.showMessageDialog(this,
	"We can't access the leaderboard right now!",
		"Oops!",
			JOptionPane.ERROR_MESSAGE);
	}


}

