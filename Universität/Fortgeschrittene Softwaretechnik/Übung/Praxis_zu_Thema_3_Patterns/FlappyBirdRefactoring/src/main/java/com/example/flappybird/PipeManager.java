package com.example.flappybird;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;

public class PipeManager {
    private List<Pipe> pipes = new ArrayList<>();
    private int pipeDistTracker = 0;

    public static final int PIPE_DISTANCE = 150;          // Horizontal distance between pipes


    public void reset() {
        pipes = new ArrayList<>();
        pipeDistTracker = 0;
    }

    public void update() {

        // Decrease distance between pipes
        pipeDistTracker--;

        // If there is no distance,
        // a new pipe is needed
        if (pipeDistTracker < 0) {
            this.pipeDistTracker = PIPE_DISTANCE;
            spawnPipePair();
        }

        for (Pipe p: pipes) {
            p.move();
        }
    }

    public boolean collide(Rectangle hitbox) {
        for (Pipe p: pipes) {
            if (p.collide(hitbox)) {
                return true;
            }
        }
        return false;
    }

    public boolean collectPoints(Rectangle hitbox) {
        for (Pipe p: pipes) {
            if (p.checkAwardPoint(hitbox)) {
                return true;
            }

        }
        return false;
    }

    public void render(Renderer renderer, Graphics g) {
        for (Pipe p: pipes) {
            p.render(renderer, g);
        }
    }

    private void spawnPipePair() {
        Pipe top = findOffscreenOrCreate();
        top.respawnAsTop();

        Pipe bottom = findOffscreenOrCreate();
        bottom.respawnAsBottom(top.getY());
    }

    private Pipe findOffscreenOrCreate() {
        for (Pipe p: pipes) {
            if (p.getX() < 0) {
                return p;
            }
        }
        Pipe p = new Pipe();
        pipes.add(p);
        return p;
    }

}
