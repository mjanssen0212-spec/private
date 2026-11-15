package com.example.flappybird;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;

public class MenuState extends GameStateAbstract{
    private Renderer renderer;
    private Ground ground;
    private GameSession gameSession;
    private GameStateAbstract nextGameState;

    public MenuState(Renderer renderer, Ground ground, GameSession gameSession) {
        this.gameSession = gameSession;
        this.renderer = renderer;
        this.ground = ground;
    }

    @Override
    public void render(Graphics g) {
        ground.render(g);
        drawMenu(g);
        gameSession.getBird().menuFloat();
    }

    @Override
    public GameStateAbstract update(Graphics g) {
        return this;
    }

    @Override
    public GameStateAbstract handleKeyEvent(KeyEvent e) {
        int keyCode = e.getKeyCode();

        if (keyCode == KeyEvent.VK_ENTER) {
            return this.nextGameState;
        }

        return this;
    }

    @Override
    public GameStateAbstract handleMouseEvent(MouseEvent e) {
        Point clickedPoint = e.getPoint();

        if(isTouching(renderer.getTextureRect("playButton"), clickedPoint)) {
            return this.nextGameState;
        } else if (isTouching(renderer.getTextureRect("leaderboard"), clickedPoint)) {
            return this;
        }

        if (gameSession.getBird().isAlive()) {

            if (isTouching(renderer.getTextureRect("rateButton"), clickedPoint)) {
                Helper.openURL("http://paulkr.com"); // Open website
            }

        }

        return this;
    }

    @Override
    public void updatePipes(Graphics g) {

    }

    public void setNextGameState(GameStateAbstract nextGameState) {
        this.nextGameState = nextGameState;
    }

//    private void startGame() {
//        currentGameState = inGameState;
//        inStartGameState = true;
//    }

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

}
