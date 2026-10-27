//1871808
//Matthias Janßen

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class EmailMatcherFuzzTest {

    private static final String LOG_FILE = "./log.txt";
    private static final int TARGET_COUNT = 100;
    private static int validEmailCount = 0;

    @FuzzTest
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        if (validEmailCount >= TARGET_COUNT) {
            System.out.println("Reached " + TARGET_COUNT + " valid email addresses. Stopping fuzzer.");
            System.exit(0);
        }

        String input = data.consumeRemainingAsString();

        if (EmailMatcher.isValidEmail(input)) {
            validEmailCount++;
            System.out.println("Valid (" + validEmailCount + "/" + TARGET_COUNT + "): " + input);

            File file = new File(LOG_FILE);
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file, true))) {
                writer.write(input);
                writer.newLine();
                writer.flush();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

            if (validEmailCount >= TARGET_COUNT) {
                System.out.println("Found " + TARGET_COUNT + " valid email addresses. Exiting.");
                System.exit(0);
            }
        }
    }
}
