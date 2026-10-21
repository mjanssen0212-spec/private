import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_40c4f3901000a4d2dc0bd359ec58a60922ec4a7f {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAABdwQAAAABdAA8bWFnaWNzdHJpbmc0Cm3AgMCAwIBDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ8CAHcCAY2FnaR3AgHRpbta0eA==");

    public static void main(String[] args) throws Throwable {
        Crash_40c4f3901000a4d2dc0bd359ec58a60922ec4a7f.class.getClassLoader().setDefaultAssertionStatus(true);
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