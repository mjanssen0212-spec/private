import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_0ef580af4ba118106cee2aefe9c1f1b9695bf170 {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAAAdwQAAAAAeA==");

    public static void main(String[] args) throws Throwable {
        Crash_0ef580af4ba118106cee2aefe9c1f1b9695bf170.class.getClassLoader().setDefaultAssertionStatus(true);
        try {
            Method fuzzerInitialize = EmailMatcherFuzzTest.class.getMethod("fuzzerInitialize");
            fuzzerInitialize.invoke(null);
        } catch (NoSuchMethodException ignored) {
            try {
                Method fuzzerInitialize = EmailMatcherFuzzTest.class.getMethod("fuzzerInitialize", String[].class);
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
        EmailMatcherFuzzTest.fuzzerTestOneInput(input);
    }
}