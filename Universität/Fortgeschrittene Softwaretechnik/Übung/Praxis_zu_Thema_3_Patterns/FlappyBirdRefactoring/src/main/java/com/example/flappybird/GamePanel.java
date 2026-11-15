package com.example.flappybird;

/**
 * GamePanel.java
 * Main game panel
 *
 * @author  Paul Krishnamurthy
 */

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.HashMap;

public class GamePanel extends JPanel implements KeyListener, MouseListener {

	
	////////////////////
	// Game variables //
	////////////////////
	private final GameSession gameSession;

	private final Renderer renderer;

	private final Ground ground;

	private final PipeManager pipeManager = new PipeManager();

	private GameStateAbstract currentGameState;

	private final MenuState menuState;
	private final InGameState inGameState;
	private final GameOverState gameOverState;

	// Textures
	private final Sprites sprites;
	public static HashMap<String, Texture> textures;
	
	// Moving base effect
	private final static int baseSpeed    = 2;
	private final static int[] baseCoords = { 0, 435 };

	
	public boolean ready = false;                   // If game has loaded

	private final Audio audio   = new Audio();


	public GamePanel () {

		this.sprites = new Sprites();
		this.textures = sprites.getGameTextures();

		this.renderer = new Renderer(textures);
		this.ground = new Ground(baseCoords, renderer, baseSpeed);
		this.gameSession = new GameSession(textures, pipeManager);

		this.menuState = new MenuState(renderer, ground, gameSession);
		this.inGameState = new InGameState(renderer, ground, gameSession, audio);
		this.gameOverState = new GameOverState(renderer, ground, gameSession);

		this.currentGameState = menuState;

		this.menuState.setNextGameState(inGameState);
		this.inGameState.setNextGameState(gameOverState);
		this.gameOverState.setNextGameState(inGameState);

		// Input listeners
		addKeyListener(this);
		addMouseListener(this);

	}

	/**
	 * To start game after everything has been loaded
	 */
	public void addNotify() {
		super.addNotify();
		requestFocus();
		ready = true;
	}

	@Override
	public void paintComponent (Graphics g) {
		super.paintComponent(g);

		Bird gameBird = gameSession.getBird();

		// Set font and color
		g.setFont(renderer.getFlappyFontReal());
		g.setColor(Color.white);

		// Background
		renderer.drawComponent(gameSession.isDarkTheme() ? "background2" : "background1", 0, 0, g);

		// Draw bird
		gameBird.renderBird(g);

		currentGameState = currentGameState.update();
		currentGameState.render(g);
	}

	//////////////////////
	// Keyboard actions //
	//////////////////////

	public void keyTyped (KeyEvent e) {}
	public void keyReleased (KeyEvent e) {}

	public void keyPressed (KeyEvent e) {
		currentGameState = currentGameState.handleKeyEvent(e);

	}

	///////////////////
	// Mouse actions //
	///////////////////

	public void mouseExited (MouseEvent e) {}
	public void mouseEntered (MouseEvent e) {}
	public void mouseReleased (MouseEvent e) {}
	public void mouseClicked (MouseEvent e) {}

	public void mousePressed (MouseEvent e) {
		currentGameState = currentGameState.handleMouseEvent(e);
	}









}

