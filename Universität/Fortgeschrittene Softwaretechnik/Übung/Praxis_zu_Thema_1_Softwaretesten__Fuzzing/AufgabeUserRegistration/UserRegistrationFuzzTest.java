//1871808
//Matthias Janßen

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class UserRegistrationFuzzTest {

    private static final String LOG_FILE = "./log.txt";
    private static final int TARGET_COUNT = 100;
    private static int validLoginCount = 0;

    @FuzzTest
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        if (validLoginCount >= TARGET_COUNT) {
            System.out.println("Reached " + TARGET_COUNT + " valid email addresses. Stopping fuzzer.");
            System.exit(0);
        }

//        String input = data.consumeRemainingAsString();

        String username = data.consumeString(15);
        String password = data.consumeString(20);
        String email = data.consumeString(100);

        try {
            if (UserRegistration.registerUser(username, password, email)) {
                validLoginCount++;
                System.out.println("Valid (" + validLoginCount + "/" + TARGET_COUNT + "): " +
                        username + ", " + password + ", " + email);

                File file = new File(LOG_FILE);
                try (BufferedWriter writer = new BufferedWriter(new FileWriter(file, true))) {
                    writer.write("username: " + username + "\n");
                    writer.write(", password: " + password + "\n");
                    writer.write(", email: " + email + "\n");
                    writer.newLine();
                    writer.flush();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }

                if (validLoginCount >= TARGET_COUNT) {
                    System.out.println("Found " + TARGET_COUNT + " valid email addresses. Exiting.");
                    System.exit(0);
                }
            }
        } catch (RegistrationException e) {

        }
    }
}
