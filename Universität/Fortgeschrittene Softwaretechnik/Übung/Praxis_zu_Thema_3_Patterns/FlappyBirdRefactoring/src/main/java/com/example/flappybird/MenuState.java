package com.example.flappybird;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;

public class MenuState extends GameStateAbstract{

    public MenuState(Renderer renderer, Ground ground, GameSession gameSession) {
        super(renderer, ground, gameSession);
    }

    @Override
    public void render(Graphics g) {
        ground.render(g);
        drawMenu(g);
    }

    @Override
    public GameStateAbstract update() {
        gameSession.getBird().menuFloat();
        ground.move();
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
            showErrorMessage();
            return this;
        }

        if (gameSession.getBird().isAlive()) {

            if (isTouching(renderer.getTextureRect("rateButton"), clickedPoint)) {
                Helper.openURL("http://paulkr.com"); // Open website
            }

        }

        return this;
    }

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
