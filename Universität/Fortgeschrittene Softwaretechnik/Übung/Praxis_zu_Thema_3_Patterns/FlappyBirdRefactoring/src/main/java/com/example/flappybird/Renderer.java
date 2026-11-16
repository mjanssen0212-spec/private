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
            drawComponent((mini ? "mini-score-" : "score-") + digits[i], drawScoreX, mini ? y : 60, g);

            // Size to add varies based on texture
            drawScoreX += digitSize(digits[i], mini);
        }

    }

    public Rectangle getTextureRect(String textureName) {
        return textures.get(textureName).getRect();
    }

    private int digitSize(char digit, boolean mini) {
        if (mini) {
            return 18;
        } else {
            return digit == '1' ? 25 : 35;
        }
    }

    public Map<String, Texture> getTextures() {
        return textures;
    }

    public Font getFlappyFontReal() {
        return flappyFontReal;
    }

    private Font getFont(int size) {
        return flappyFontBase.deriveFont(Font.PLAIN, size);
    }
}
