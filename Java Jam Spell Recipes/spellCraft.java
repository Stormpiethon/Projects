import java.util.*;

public class spellCraft {
    // Powers categorized by Light and Dark
    static Map<String, List<String>> powers = Map.of(
            "Light", Arrays.asList("Honor", "Love", "Joy", "Compassion", "Hope", "Kindness", "Courage", "Patience", "Trust", "Justice"),
            "Dark", Arrays.asList("Hatred", "Lust", "Fear", "Anger", "Greed", "Pride", "Despair", "Envy", "Wrath", "Shame"));

    // Materials categorized by elemental type
    static Map<String, List<String>> materials = Map.of(
            "Earth", Arrays.asList("Dirt", "Rocks", "Clay", "Sand", "Quartz"),
            "Wind", Arrays.asList("Air", "Leaves", "Ashes", "Sulfur", "Crystal"),
            "Water", Arrays.asList("Water", "Ice", "Oil", "Silver", "Gold"),
            "Fire", Arrays.asList("Lava", "Iron", "Steel", "Copper", "Fire"));

    // Magic Words categorized by group
    static Map<String, List<String>> magicWords = Map.of(
            "Group A", Arrays.asList("Elanor", "Nimrais", "Alduin", "Melkor", "Luthien"),
            "Group B", Arrays.asList("Oronar", "Eärendil", "Fëanor", "Galad", "Thalion"),
            "Group C", Arrays.asList("Calanon", "Hithar", "Mithril", "Valar", "Gond"),
            "Group D", Arrays.asList("Elenion", "Anor", "Morgul", "Tauriel", "Silmaril"));

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Game Setup
        int userHealth = 100;
        int opponentHealth = 100;
        int rounds = 5;

        System.out.println("\n\n\t ***** Welcome to the Spell Crafting Game! *****");
        System.out.println("You will choose ingredients to create spells to use in a match against an opponent.");

        // Game Loop
        // Game Loop
        for (int i = 1; i <= rounds; i++) {
            System.out.println("===========================================================================");
            System.out.println("\t--- Round " + i + " ---");
            System.out.println("\tYour Health: " + userHealth);
            System.out.println("\tOpponent Health: " + opponentHealth);

            // Step 1: User chooses an emotion (flattened list of options from all categories)
            System.out.println("\nStep 1: Choose an emotion:");
            List<String> emotionOptions = getRandomOptions(powers);
            displayOptions(emotionOptions);
            String chosenEmotion = emotionOptions.get(scanner.nextInt() - 1);
            String emotionCategory = findCategory(powers, chosenEmotion);

            // Step 2: User chooses a material (flattened list of options from all categories)
            System.out.println("\nStep 2: Choose a material:");
            List<String> materialOptions = getRandomOptions(materials);
            displayOptions(materialOptions);
            String chosenMaterial = materialOptions.get(scanner.nextInt() - 1);
            String materialCategory = findCategory(materials, chosenMaterial);

            // Step 3: User chooses a magic word (flattened list of options from all
            System.out.println("\nStep 3: Choose a magic word:");
            List<String> magicWordOptions = getRandomOptions(magicWords);
            displayOptions(magicWordOptions);
            String chosenMagicWord = magicWordOptions.get(scanner.nextInt() - 1);
            String magicWordGroup = findCategory(magicWords, chosenMagicWord);

            // Determine the result of the user's spell
            String userSpellResult = determineSpellResult(emotionCategory, materialCategory, magicWordGroup);

            // Step 1: Opponent chooses an emotion (random)
            String opponentEmotionCategory = randomKey(powers);
            List<String> opponentEmotionOptions = powers.get(opponentEmotionCategory);
            String opponentChosenEmotion = opponentEmotionOptions.get(new Random().nextInt(opponentEmotionOptions.size()));

            // Step 2: Opponent chooses a material (random)
            String opponentMaterialCategory = randomKey(materials);
            List<String> opponentMaterialOptions = materials.get(opponentMaterialCategory);
            String opponentChosenMaterial = opponentMaterialOptions.get(new Random().nextInt(opponentMaterialOptions.size()));

            // Step 3: Opponent chooses a magic word (random)
            String opponentMagicWordGroup = randomKey(magicWords);
            List<String> opponentMagicWordOptions = magicWords.get(opponentMagicWordGroup);
            String opponentChosenMagicWord = opponentMagicWordOptions.get(new Random().nextInt(opponentMagicWordOptions.size()));

            // Determine the result of the opponent's spell
            String opponentSpellResult = determineSpellResult(opponentEmotionCategory, opponentMaterialCategory, opponentMagicWordGroup);

            // Display the User's results
            System.out.println("==================================================================");
            System.out.println("\n You chose:");
            System.out.println("Emotion: " + chosenEmotion);
            System.out.println("Material: " + chosenMaterial);
            System.out.println("Magic Word: " + chosenMagicWord);
            System.out.println("Your spell result: " + userSpellResult);

            // Display the opponent's results
            System.out.println("\nOpponent chose:");
            System.out.println("Emotion: " + opponentChosenEmotion);
            System.out.println("Material: " + opponentChosenMaterial);
            System.out.println("Magic Word: " + opponentChosenMagicWord);
            System.out.println("Opponent's spell result: " + opponentSpellResult);
            System.out.println("==================================================================");

            // Handle health changes based on outcomes (cancel logic)
            if (!userSpellResult.equals("Cancel Opponent Spell")
                    && !opponentSpellResult.equals("Cancel Opponent Spell")) {
                // Apply effects to health if no cancel occurred
                switch (userSpellResult) {
                    case "Damage Opponent":
                        opponentHealth -= 20;
                        System.out.println("Your spell damages the opponent by 20 HP!");
                        break;
                    case "Heal Self":
                        userHealth += 15;
                        System.out.println("Your spell heals you for 15 HP!");
                        break;
                    case "Backfire":
                        userHealth -= 10;
                        System.out.println("Your spell backfires and damages you for 10 HP!");
                        break;
                    case "Cancel Opponent Spell":
                        // If cancel occurred, no changes to health
                        System.out.println("Your spell cancels the opponent's spell!");
                        break;
                    default:
                        System.out.println("Your spell fizzles and does nothing.");
                }

                switch (opponentSpellResult) {
                    case "Damage Opponent":
                        userHealth -= 20;
                        System.out.println("The opponent's spell damages you by 20 HP!");
                        break;
                    case "Heal Self":
                        opponentHealth += 15;
                        System.out.println("The opponent's spell heals them for 15 HP!");
                        break;
                    case "Backfire":
                        opponentHealth -= 10;
                        System.out.println("The opponent's spell backfires and damages them for 10 HP!");
                        break;
                    case "Cancel Opponent Spell":
                        // If cancel occurred, no changes to health
                        System.out.println("The opponent's spell cancels your spell!");
                        break;
                    default:
                        System.out.println("The opponent's spell fizzles and does nothing.");
                }
            }

            // Check if someone has won
            if (userHealth <= 0 || opponentHealth <= 0) {
                break;
            }
        }

        // Declare the winner
        if (userHealth > opponentHealth) {
            System.out.println("\nCongratulations! You win!");
        } else if (opponentHealth > userHealth) {
            System.out.println("\nYour opponent wins. Better luck next time!");
        } else {
            System.out.println("\nIt's a tie!");
        }

        scanner.close();
    }

    // Function to get a random key from a dictionary
    public static <K, V> K randomKey(Map<K, V> map) {
        List<K> keys = new ArrayList<>(map.keySet());
        return keys.get(new Random().nextInt(keys.size()));
    }

    // Function to display options for the user
    public static void displayOptions(List<String> options) {
        for (int i = 0; i < options.size(); i++) {
            System.out.println((i + 1) + ": " + options.get(i));
        }
        System.out.print("Enter your choice (1-" + options.size() + "): ");
    }

    // Helper method to get random options from any dictionary
    public static List<String> getRandomOptions(Map<String, List<String>> dictionary) {
        // Initialize a list to store all options
        List<String> allOptions = new ArrayList<>();

        // Add all values from the dictionary to the list
        for (List<String> values : dictionary.values()) {
            allOptions.addAll(values);
        }
        /// Shuffle the list to get random order and return the first 5
        Collections.shuffle(allOptions);
        return allOptions.subList(0, Math.min(5, allOptions.size()));
    }

    // Helper method to find the category of a selected value
    public static String findCategory(Map<String, List<String>> dictionary, String value) {
        for (Map.Entry<String, List<String>> entry : dictionary.entrySet()) {
            if (entry.getValue().contains(value)) {
                return entry.getKey();
            }
        }
        return null; // Shouldn't happen if value is valid
    }

    // Function to determine the result of the spell
    public static String determineSpellResult(String emotion, String material, String magicWord) {
        // Define spell outcomes
        Map<String, String> outcomes = Map.ofEntries(
                Map.entry("Light-Earth-Group A", "Heal Self"),
                Map.entry("Light-Earth-Group B", "Damage Opponent"),
                Map.entry("Light-Earth-Group C", "Damage Opponent"),
                Map.entry("Light-Earth-Group D", "Cancel Opponent Spell"),
                Map.entry("Light-Air-Group A", "Damage Opponent"),
                Map.entry("Light-Air-Group B", "Heal Self"),
                Map.entry("Light-Air-Group C", "Backfire"),
                Map.entry("Light-Air-Group D", "Damage Opponent"),
                Map.entry("Light-Water-Group A", "Cancel Opponent Spell"),
                Map.entry("Light-Water-Group B", "Damage Opponent"),
                Map.entry("Light-Water-Group C", "Heal Self"),
                Map.entry("Light-Water-Group D", "Damage Opponent"),
                Map.entry("Light-Fire-Group A", "Damage Opponent"),
                Map.entry("Light-Fire-Group B", "Backfire"),
                Map.entry("Light-Fire-Group C", "Heal Self"),
                Map.entry("Light-Fire-Group D", "Damage Opponent"),
                Map.entry("Dark-Earth-Group A", "Damage Opponent"),
                Map.entry("Dark-Earth-Group B", "Heal Self"),
                Map.entry("Dark-Earth-Group C", "Damage Opponent"),
                Map.entry("Dark-Earth-Group D", "Cancel Opponent Spell"),
                Map.entry("Dark-Air-Group A", "Damage Opponent"),
                Map.entry("Dark-Air-Group B", "Heal Self"),
                Map.entry("Dark-Air-Group C", "Damage Opponent"),
                Map.entry("Dark-Air-Group D", "BackFire"),
                Map.entry("Dark-Water-Group A", "Cancel Opponent Spell"),
                Map.entry("Dark-Water-Group B", "Damage Opponent"),
                Map.entry("Dark-Water-Group C", "Heal Self"),
                Map.entry("Dark-Water-Group D", "Damage Opponent"),
                Map.entry("Dark-Fire-Group A", "Damage Opponent"),
                Map.entry("Dark-Fire-Group B", "Damage Opponent"),
                Map.entry("Dark-Fire-Group C", "Heal Self"),
                Map.entry("Dark-Fire-Group D", "Backfire"));

        // Build the combination key
        String key = emotion + "-" + material + "-" + magicWord;

        // Return the result, defaulting to "Fizzle" if no match is found
        return outcomes.getOrDefault(key, "Fizzle");
    }
    

}