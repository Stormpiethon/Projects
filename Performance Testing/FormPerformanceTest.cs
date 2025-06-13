using System.Diagnostics;

namespace Performance_Testing
{
    public partial class FormPerformanceTest : Form
    {
        public FormPerformanceTest()
        {
            InitializeComponent();
        }

        // Button click will take user input from the text box and check for correct values
        // Must be between 0 and 100,000
        private void button1_Click(object sender, EventArgs e)
        {
            // Get the text value from the text box and make sure it is a valid integer within the specified range
            string input = textBoxUserInput.Text;
            bool valid = int.TryParse(input, out int value) && value >= 0 && value <= 100000;

            // Logic for next step based on validity of the input
            if (!valid)
            {
                // If invalid, display a message box with an error and clear the text box input field
                MessageBox.Show("Please enter a valid number between 0 and 100,000.", "Invalid Input", MessageBoxButtons.OK, MessageBoxIcon.Error);
                textBoxUserInput.Clear();
            }
            else
            {

                // =============== Array Creation and Population Performance Test ===============
                // Create a stopwatch to time how long it takes to create the array and populate it
                Stopwatch stopwatch = new Stopwatch();
                stopwatch.Start();

                // Run the performance test by using the input value and make an array of that size
                int[] array = new int[value];

                // Instantiate a new Random object that will be used to populate the array
                Random randy = new Random();

                // Populate the array with random integers between 0 and 10000
                for (int i = 0; i < array.Length; i++)
                {
                    array[i] = randy.Next(0, 10001);
                }

                // Stop the timer and store the elapsed time in milliseconds
                stopwatch.Stop();
                double buildTime = stopwatch.Elapsed.TotalMilliseconds;

                // Display the buildTime value to the label on the form
                labelBuildTime.ForeColor = Color.Black;
                labelBuildTime.Text = $"Time to make array: {buildTime} ms";


                // =============== Sorting Performance Test ===============
                // Reset the stopwatch and start it for the sorting performance test
                stopwatch.Reset();
                stopwatch.Start();

                // Sort the array using Array.Sort method
                Array.Sort(array);

                // Stop the timer and store the elapsed time in milliseconds
                stopwatch.Stop();
                double sortTime = stopwatch.Elapsed.TotalMilliseconds;

                // Display the sortTime value to the label on the form
                labelSortTime.ForeColor = Color.Black;
                labelSortTime.Text = $"Time to sort array: {sortTime} ms";

                // =============== Progress Bar Updates ===============
                // Fill the progress bar completely next to the label that has the slowest time
                // Calculate the percentage of the slower time that the faster time is and adjust other progress bar
                if (buildTime > sortTime)
                {
                    progressBarBuildTime.Value = 100;
                    progressBarSortTime.Value = (int)(sortTime / buildTime * 100);
                }
                else
                {
                    progressBarSortTime.Value = 100;
                    progressBarBuildTime.Value = (int)(buildTime / sortTime * 100);
                }
            }
        }
    }
}
