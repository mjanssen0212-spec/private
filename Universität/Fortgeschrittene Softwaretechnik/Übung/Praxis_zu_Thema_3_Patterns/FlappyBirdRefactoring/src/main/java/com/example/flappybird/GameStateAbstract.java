package com.example.flappybird;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;

public abstract class GameStateAbstract{

    public abstract void render(Graphics g);
    public abstract GameStateAbstract update(Graphics g);
    public abstract GameStateAbstract handleKeyEvent(KeyEvent e);
    public abstract GameStateAbstract handleMouseEvent(MouseEvent e);
    public abstract void updatePipes(Graphics g);

    /**
     * Checks if point is in rectangle
     *
     * @param      r     Rectangle
     * @return           Boolean if point collides with rectangle
     */
    protected boolean isTouching (Rectangle r, Point clickedPoint) {
        return r.contains(clickedPoint);
    }
}
