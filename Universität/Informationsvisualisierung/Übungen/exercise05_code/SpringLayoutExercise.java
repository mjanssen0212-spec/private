package iv.graph;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

# see Page 72ff in
# Kaufmann, M., & Wagner, D. (Eds.). (2003). Drawing graphs: methods and models. Springer.

public class SpringLayoutExercise extends Application {

    final int canvasWidth = 800;
    final int canvasHeight = 800;
    final double naturalLength = 60;
    final double deltaInit = 0.5;
    final double cRho = Math.pow(naturalLength, 3) / 2.0;
    final double cSigma = naturalLength * 5;
    int currentIteration = 0;

    boolean single_step = true;

    Random random = new Random();

    class Node {
        String label;
        double x, y;
        Vec force = new Vec(0,0);

        Node(String label) {
            this.label = label;
            this.x = 50 + random.nextDouble() * (canvasWidth - 100);
            this.y = 50 + random.nextDouble() * (canvasHeight - 100);
        }
    }

    class Graph {
        List<Node> nodes;
        List<Edge> edges;

        Graph(List<Node> nodes, List<Edge> edges) {
            this.nodes = nodes;
            this.edges = edges;
        }

        boolean containsEdge(Node src, Node trgt) {
            return edges.stream().anyMatch(e -> (e.source == src && e.target == trgt)
                                            || (e.source == trgt && e.target == src));
        }
    }

    class Edge {
        Node source, target;

        Edge(Node source, Node target) {
            this.source = source;
            this.target = target;
        }
    }

    Graph createRandomGraph(int n, int m) {
        Graph graph = new Graph(new ArrayList<>(), new ArrayList<>());

        for (int i = 0; i < n; i++) {
            graph.nodes.add(new Node(String.valueOf(i + 1)));
        }

        while (graph.edges.size() < m) {
            Node src = graph.nodes.get(random.nextInt(n));
            Node tgt = graph.nodes.get(random.nextInt(n));
            if (src != tgt && !graph.containsEdge(src,tgt)) {
                graph.edges.add(new Edge(src, tgt));
            }
        }
        return graph;
    }

    class Vec {
        double x;
        double y;

        Vec(double x, double y) { this.x = x; this.y = y; }

        Vec(Node node) { this.x = node.x; this.y = node.y; }

        double length() { return Math.sqrt(x * x + y * y); }

        Vec subtract(Vec v) { return new Vec(this.x - v.x, this.y - v.y); }

        Vec add(Vec v) { return new Vec(this.x + v.x, this.y + v.y); }

        Vec mult(double k) { return new Vec(k*this.x , k*this.y); }

        Vec div(double k) { return new Vec(this.x/k , this.y/k); }

        Vec unitVectorTo(Vec target) {
            Vec v = target.subtract(this);
            double len = v.length();
            return len == 0 ? new Vec(0, 0) : v.div(len);
        }
    }



    double anneal(double d, int i, int max) {
        // Select one of the following annealing schemes
        // return i>max ? 0 : Math.pow(d,(i*12)/maxi+1) // EXPONENTIAL
        // return i>max ? 0 : d-(i*d/maxi) // LINEAR
        return d / Math.log(i + 2); // LOGARITHMIC
        // return d; // CONSTANT
    }

    void computeForces(Graph graph) {
        // computes the values of variable force for each node
      return;
    }

    void updatePositions(Graph graph, double delta) {
        //# computes new x and y values for each node
        return;
    }

    void computeLayout(Graph graph, int iterations) {
        for (int t = 0; t < iterations; t++) {
            double delta = anneal(deltaInit, t, iterations);
            computeForces(graph);
            updatePositions(graph, delta);
        }
    }

    void drawGraph(GraphicsContext gc, Graph g) {
        gc.clearRect(0, 0, canvasWidth, canvasHeight);

        gc.setStroke(Color.GRAY);
        for (Edge e : g.edges) {
            gc.strokeLine(e.source.x, e.source.y, e.target.x, e.target.y);
        }

        gc.setFill(Color.LIGHTGREEN);
        gc.setFont(Font.font("Helvetica", 12));
        for (Node n : g.nodes) {
            gc.fillOval(n.x - 15, n.y - 15, 30, 30);
            gc.setFill(Color.BLUE);
            gc.fillText(n.label, n.x - 5, n.y + 5);
            gc.setFill(Color.LIGHTGREEN);
        }
    }

    @Override
    public void start(Stage stage) {
        Canvas canvas = new Canvas(canvasWidth, canvasHeight);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        Graph graph = createRandomGraph(15, 20);

        Timeline timeline = new Timeline(new KeyFrame(Duration.millis(50), e -> {
            if (currentIteration < 100) {
                double delta = anneal(deltaInit, currentIteration++, 100);
                computeForces(graph);
                updatePositions(graph, delta);
                drawGraph(gc, graph);

            }}));

            timeline.setCycleCount(100);
            timeline.play();

        Pane root = new Pane(canvas);
        stage.setScene(new Scene(root));
        stage.setTitle("Force-Directed Graph Layout (Eades 1984)");
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}