import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_4dc0c6215edc0a894066b40607a2f17888d214b7 {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAABdwQAAAABdAAkbWFnaWNzdHJpbmc0aWlpaRZpaWlpaW1hZ0NjaRZpaWlpaXI0eA==");

    public static void main(String[] args) throws Throwable {
        Crash_4dc0c6215edc0a894066b40607a2f17888d214b7.class.getClassLoader().setDefaultAssertionStatus(true);
        try {
            Method fuzzerInitialize = ExampleFuzzer.class.getMethod("fuzzerInitialize");
            fuzzerInitialize.invoke(null);
        } catch (NoSuchMethodException ignored) {
            try {
                Method fuzzerInitialize = ExampleFuzzer.class.getMethod("fuzzerInitialize", String[].class);
                fuzzerInitialize.invoke(null, (Object) args);
            } catch (NoSuchMethodException ignored1) {
            } catch (IllegalAccessException | InvocationTargetException e) {
                e.printStackTrace();
                System.exit(1);
            }
        } catch (IllegalAccessException | InvocationTargetException e) {
            e.printStackTrace();
            System.exit(1);
        }
        com.code_intelligence.jazzer.api.CannedFuzzedDataProvider input = new com.code_intelligence.jazzer.api.CannedFuzzedDataProvider(base64Bytes);
        ExampleFuzzer.fuzzerTestOneInput(input);
    }
}