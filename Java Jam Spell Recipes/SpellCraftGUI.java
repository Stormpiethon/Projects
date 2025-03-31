import javax.swing.*;
import java.awt.*;
import java.util.*;
import java.util.List;

public class SpellCraftGUI {

    // Add a stage variable for which stage of the spell is being chosen
    private static int stage = 1;

    // // Variable to store the selected keys
    private static StringBuilder selectedKeys = new StringBuilder();

    // Powers categorized by Light and Dark
    static Map<String, List<String>> powers = Map.of(
            "Light", Arrays.asList("Honor", "Love", "Joy", "Compassion", "Hope", 
            "Kindness", "Courage", "Patience", "Trust", "Justice"),
            "Dark", Arrays.asList("Hatred", "Lust", "Fear", "Anger", "Greed", 
            "Pride", "Despair", "Envy", "Wrath", "Shame"));

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

    // Define spell outcomes
    static Map<String, String> outcomes = Map.ofEntries(
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

    public static void main(String[] args) {
        // Create the main JFrame
        JFrame frame = new JFrame("Spell Crafting Game");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 400);
        frame.setLayout(new BorderLayout(10, 10));

        // Health bars panel
        JPanel healthPanel = new JPanel(new GridLayout(2, 1, 10, 10));

        // User health bar
        JLabel userHealthLabel = new JLabel("User Health:");
        JProgressBar userHealthBar = new JProgressBar(0, 100);
        userHealthBar.setValue(100);
        userHealthBar.setStringPainted(true);

        // Opponent health bar
        JLabel opponentHealthLabel = new JLabel("Opponent Health:");
        JProgressBar opponentHealthBar = new JProgressBar(0, 100);
        opponentHealthBar.setValue(100);
        opponentHealthBar.setStringPainted(true);

        healthPanel.add(userHealthLabel);
        healthPanel.add(userHealthBar);
        healthPanel.add(opponentHealthLabel);
        healthPanel.add(opponentHealthBar);

        // Text area to display user choices
        JTextArea userChoicesArea = new JTextArea(5, 30);
        userChoicesArea.setEditable(false);
        userChoicesArea.setBorder(BorderFactory.createTitledBorder("Recipe"));
        userChoicesArea.setText("Choose your spell ingredients:\n");

        // Image labels for spell effects
        JLabel userSpellEffectLabel = new JLabel();
        userSpellEffectLabel.setPreferredSize(new Dimension(150, 150));
        userSpellEffectLabel.setOpaque(true);
        userSpellEffectLabel.setBackground(Color.LIGHT_GRAY);

        JLabel opponentSpellEffectLabel = new JLabel();
        opponentSpellEffectLabel.setPreferredSize(new Dimension(150, 150));
        opponentSpellEffectLabel.setOpaque(true);
        opponentSpellEffectLabel.setBackground(Color.LIGHT_GRAY);

        // Buttons panel (5 buttons added)
        JPanel buttonPanel = new JPanel(new GridLayout(1, 5, 10, 10));
        List<String> currentOptions = getRandomOptions(powers);
        updateButtons(buttonPanel, currentOptions, userChoicesArea);

        // Frame layout
        frame.add(healthPanel, BorderLayout.NORTH);
        frame.add(userChoicesArea, BorderLayout.CENTER);
        frame.add(userSpellEffectLabel, BorderLayout.WEST);
        frame.add(opponentSpellEffectLabel, BorderLayout.EAST);
        frame.add(buttonPanel, BorderLayout.SOUTH);

        // Make frame visible
        frame.setVisible(true);
    }

    private static List<String> getRandomOptions(Map<String, List<String>> map) {
        List<String> options = new ArrayList<>();
        for (List<String> values : map.values()) {
            options.addAll(values);
        }
        Collections.shuffle(options);
        return options.subList(0, 5);
    }

    private static void updateButtons(JPanel buttonPanel, List<String> options, JTextArea userChoicesArea, int stage) {
        buttonPanel.removeAll();
        for (String option : options) {
            JButton button = new JButton(option);
            button.addActionListener(e -> {
                String selectedKey = null;

                // Determine which map to pass to lookupKey based on the stage
                if (stage == 1) {
                    selectedKey = lookupKey(option, powers);
                } else if (stage == 2) {
                    selectedKey = lookupKey(option, materials);
                } else if (stage == 3) {
                    selectedKey = lookupKey(option, magicWords);
                }

                // Append the selected key to the user choices
                if (selectedKey != null) {
                    userChoicesArea.append(selectedKey + "\n");
                    selectedKeys.append(selectedKey).append("-");
                }

                // Increment stage, and reset to 1 after the third stage
                stage++;
                if (stage > 3) {
                    stage = 1; // Reset to stage 1 for the next round
                    List<String> newOptions = getOptionsForStage(stage);
                    updateButtons(buttonPanel, newOptions);
                }
            });
            buttonPanel.add(button);
        }
        buttonPanel.revalidate();
        buttonPanel.repaint();
    }

    // Helper method to get options for the current stage
    private static List<String> getOptionsForStage(int stage) {
        if (stage == 1) {
            return getRandomOptions(powers); // Powers for stage 1
        } else if (stage == 2) {
            return getRandomOptions(materials); // Materials for stage 2
        } else {
            return getRandomOptions(magicWords); // Magic words for stage 3
        }
    }

    // Helper method to lookup the key based on the value
    private static String lookupKey(String value, Map<String, List<String>> map) {
        for (Map.Entry<String, List<String>> entry : map.entrySet()) {
            if (entry.getValue().contains(value)) {
                // Return the key if the value is found in the list
                return entry.getKey();
            }
        }
        return null;
    }

}

