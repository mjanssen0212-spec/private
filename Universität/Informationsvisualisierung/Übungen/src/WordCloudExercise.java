package iv.wordcloud;

import javafx.application.Application;
import javafx.geometry.Bounds;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.util.*;

public class WordCloudExercise extends Application {

    // sample data for word cloud
    private static final Map<String, Double> data = new LinkedHashMap<>();
    static {
        data.put("Emilia", 4.2);
        data.put("Noah", 3.8);
        data.put("Sophia", 3.5);
        data.put("Matteo", 3.3);
        data.put("Emma", 3.1);
        data.put("Liam", 2.9);
        data.put("Mia", 2.8);
        data.put("Elias", 2.7);
        data.put("Hannah", 2.5);
        data.put("Leon", 2.4);
        data.put("Lina", 2.3);
        data.put("Ben", 2.2);
        data.put("Ella", 2.1);
        data.put("Paul", 2.0);
        data.put("Marie", 1.9);
        data.put("Felix", 1.8);
        data.put("Anna", 1.7);
        data.put("Lukas", 1.6);
        data.put("Lea", 1.5);
        data.put("Maximilian", 1.4);
    }

    private static final Color[] COLORS = {
            Color.RED, Color.DARKORANGE, Color.PINK,
            Color.BROWN, Color.PURPLE, Color.BLUE, Color.GRAY
    };

    private static final String[] FONT_FAMILIES = {"Arial", "Helvetica", "Times New Roman", "Courier New"};

    private static final double CANVAS_WIDTH = 500;
    private static final double CANVAS_HEIGHT = 500;

    @Override
    public void start(Stage primaryStage) {
        Pane canvas = new Pane();
        canvas.setPrefSize(CANVAS_WIDTH, CANVAS_HEIGHT);
        canvas.setStyle("-fx-background-color: white;");

        drawWordCloud(canvas, data);

        Scene scene = new Scene(canvas);
        primaryStage.setTitle("Simple Word Cloud mit JavaFX");
        primaryStage.setScene(scene);
        primaryStage.setResizable(false);
        primaryStage.show();
    }

    private void drawWordCloud(Pane canvas, Map<String, Double> data) {
        List<WordBox> placedBoxes = new ArrayList<>();
        List<WordBox> boxes = computeBoxes(data);

        // sort descending by weight
        boxes.sort((b1, b2) -> Double.compare(b2.weight, b1.weight));

        for (WordBox box : boxes) {
            if (placeBox(box, placedBoxes)) {
                box.drawBox(canvas, false);
            }
        }
    }

    private List<WordBox> computeBoxes(Map<String, Double> data) {
        double maxValue = Collections.max(data.values());
        double maxFontSize = 32;
        Random rand = new Random();
        List<WordBox> boxes = new ArrayList<>();

        for (Map.Entry<String, Double> entry : data.entrySet()) {
            String text = entry.getKey();
            double value = entry.getValue();

            int fontSize = (int) Math.round((Math.log10(value) / Math.log10(maxValue)) * maxFontSize);
            fontSize = Math.max(8, fontSize);

            String fontFamily = FONT_FAMILIES[rand.nextInt(FONT_FAMILIES.length)];
            Color color = COLORS[rand.nextInt(COLORS.length)];

            // create a tempory text object to compute the exact sizes
            Text tempText = new Text(text);
            tempText.setFont(Font.font(fontFamily, fontSize));
            Bounds bounds = tempText.getLayoutBounds();

            boxes.add(new WordBox(text, value, bounds.getWidth(), bounds.getHeight(), fontFamily, fontSize, color));
        }
        return boxes;
    }

    private boolean placeBox(WordBox box, List<WordBox> placedBoxes) {
        return true;
        // 1. Move the box along the Archimedian Spiral until
        // there is no collision with already placed boxes
        // Note: Spiral starts at center of canvas
        // 2. Add box to placed_boxes and return True
        // 3. If box could not be placed return False

    }

    public static void main(String[] args) {
        launch(args);
    }

    // inner class for boxes
    static class WordBox {
        String word;
        double weight;
        double x, y;
        double width, height;
        String fontFamily;
        int fontSize;
        Color color;

        public WordBox(String word, double weight, double width, double height, String fontFamily, int fontSize, Color color) {
            this.word = word;
            this.weight = weight;
            this.width = width;
            this.height = height;
            this.fontFamily = fontFamily;
            this.fontSize = fontSize;
            this.color = color;
        }

        public void drawBox(Pane canvas, boolean framed) {
            Text textNode = new Text(this.word);
            textNode.setFont(Font.font(this.fontFamily, this.fontSize));
            textNode.setFill(this.color);

            // Standardmäßig nutzt JavaFX die Baseline für Text.
            // With TextOrigin.TOP we set the anchor similar to Tkinter "nw" (top left)
            textNode.setTextOrigin(javafx.geometry.VPos.TOP);
            textNode.setX(this.x);
            textNode.setY(this.y);

            canvas.getChildren().add(textNode);

            if (framed) {
                Rectangle rect = new Rectangle(this.x, this.y, this.width, this.height);
                rect.setFill(Color.TRANSPARENT);
                rect.setStroke(Color.RED);
                canvas.getChildren().add(rect);
            }
        }

        public boolean checkCollision(List<WordBox> boxes) {
            for (WordBox box : boxes) {
                if (this.x + this.width < box.x || box.x + box.width < this.x) {
                    continue;
                }
                if (this.y + this.height < box.y || box.y + box.height < this.y) {
                    continue;
                }
                return true;
            }
            return false;
        }
    }
}