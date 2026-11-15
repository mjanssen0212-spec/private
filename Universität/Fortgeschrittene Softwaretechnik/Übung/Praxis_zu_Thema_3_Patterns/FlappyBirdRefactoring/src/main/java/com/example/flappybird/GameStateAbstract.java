package com.example.flappybird;

import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;

public abstract class GameStateAbstract{

    protected Renderer renderer;
    protected Ground ground;
    protected GameSession gameSession;
    protected GameStateAbstract nextGameState;

    public abstract void render(Graphics g);
    public abstract GameStateAbstract update();
    public abstract GameStateAbstract handleKeyEvent(KeyEvent e);
    public abstract GameStateAbstract handleMouseEvent(MouseEvent e);

    public void onEnter() {

    };

    public GameStateAbstract(Renderer renderer, Ground ground, GameSession gameSession) {
        this.renderer = renderer;
        this.ground = ground;
        this.gameSession = gameSession;
    }

    public void setNextGameState(GameStateAbstract nextGameState) {
        this.nextGameState = nextGameState;
    }

    /**
     * Checks if point is in rectangle
     *
     * @param      r     Rectangle
     * @return           Boolean if point collides with rectangle
     */
    protected boolean isTouching (Rectangle r, Point clickedPoint) {
        return r.contains(clickedPoint);
    }

    protected void showErrorMessage() {
        JOptionPane.showMessageDialog(null,
                "We can't access the leaderboard right now!",
                "Oops!",
                JOptionPane.ERROR_MESSAGE);
    }
}
