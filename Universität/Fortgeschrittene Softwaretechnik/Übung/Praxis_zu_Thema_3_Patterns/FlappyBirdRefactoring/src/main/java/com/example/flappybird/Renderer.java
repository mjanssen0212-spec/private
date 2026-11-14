package com.example.flappybird;

import java.awt.*;
import java.io.BufferedInputStream;
import java.io.InputStream;
import java.util.Map;

public class Renderer {
    private final Map<String, Texture> textures;

    // Fonts
    private Font flappyFontBase,
            flappyFontReal,
            flappyScoreFont,
            flappyMiniFont = null;

    public Renderer(Map<String, Texture> textures) {
        this.textures = textures;

        // Try to load ttf file
        try {
            InputStream is = new BufferedInputStream(this.getClass().getResourceAsStream("/res/fonts/flappy-font.ttf"));
            flappyFontBase = Font.createFont(Font.TRUETYPE_FONT, is);

            // Header and sub-header fonts
            flappyScoreFont = getFont(50);
            flappyFontReal  = getFont(20);
            flappyMiniFont  = getFont(15);

        } catch (Exception ex) {

            // Exit is font cannot be loaded
            ex.printStackTrace();
            System.err.println("Could not load Flappy Font!");
            System.exit(-1);
        }
    }

    public void drawComponent(String component, Graphics g) {
        Texture texture = textures.get(component);
        drawComponent(component, texture.getX(), texture.getY(), g);
    }

    public void drawComponent(String component, int x, Graphics g) {
        drawComponent(component, x, textures.get(component).getY(), g);
    }

    public void drawComponent(String component, int x, int y, Graphics g) {
        g.drawImage(textures.get(component).getImage(), x, y, null);
    }

    public void drawCredits(String s1, String s2, Graphics g) {
        drawCentered(s1, FlappyBird.WIDTH, FlappyBird.HEIGHT, 600, g);
        g.setFont(flappyMiniFont); // Change font
        drawCentered(s2, FlappyBird.WIDTH, FlappyBird.HEIGHT, 630, g);

    }

    public void drawCentered (String s, int w, int h, int y, Graphics g) {
        FontMetrics fm = g.getFontMetrics();

        // Calculate x-coordinate based on string length and width
        int x = (w - fm.stringWidth(s)) / 2;
        g.drawString(s, x, y);
    }

    public Map<String, Texture> getTextures() {
        return textures;
    }

    public Font getFlappyFontBase() {
        return flappyFontBase;
    }

    public void setFlappyFontBase(Font flappyFontBase) {
        this.flappyFontBase = flappyFontBase;
    }

    public Font getFlappyFontReal() {
        return flappyFontReal;
    }

    public void setFlappyFontReal(Font flappyFontReal) {
        this.flappyFontReal = flappyFontReal;
    }

    public Font getFlappyScoreFont() {
        return flappyScoreFont;
    }

    public void setFlappyScoreFont(Font flappyScoreFont) {
        this.flappyScoreFont = flappyScoreFont;
    }

    public Font getFlappyMiniFont() {
        return flappyMiniFont;
    }

    public void setFlappyMiniFont(Font flappyMiniFont) {
        this.flappyMiniFont = flappyMiniFont;
    }

    private Font getFont(int size) {
        return flappyFontBase.deriveFont(Font.PLAIN, size);
    }
}
