namespace Performance_Testing
{
    partial class FormPerformanceTest
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            labelDirections = new Label();
            labelBuildTime = new Label();
            labelSortTime = new Label();
            button1 = new Button();
            textBoxUserInput = new TextBox();
            progressBarBuildTime = new ProgressBar();
            progressBarSortTime = new ProgressBar();
            SuspendLayout();
            // 
            // labelDirections
            // 
            labelDirections.AutoSize = true;
            labelDirections.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelDirections.Location = new Point(212, 9);
            labelDirections.Name = "labelDirections";
            labelDirections.Size = new Size(386, 84);
            labelDirections.TabIndex = 1;
            labelDirections.Text = "Enter a number between 0 and 100,000.\r\nThis will be the size of the array that is used\r\nfor the performance test.";
            labelDirections.TextAlign = ContentAlignment.TopCenter;
            // 
            // labelBuildTime
            // 
            labelBuildTime.AutoSize = true;
            labelBuildTime.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelBuildTime.ForeColor = SystemColors.ActiveBorder;
            labelBuildTime.Location = new Point(212, 185);
            labelBuildTime.Name = "labelBuildTime";
            labelBuildTime.Size = new Size(179, 28);
            labelBuildTime.TabIndex = 2;
            labelBuildTime.Text = "Time to make array";
            // 
            // labelSortTime
            // 
            labelSortTime.AutoSize = true;
            labelSortTime.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelSortTime.ForeColor = SystemColors.ActiveBorder;
            labelSortTime.Location = new Point(212, 213);
            labelSortTime.Name = "labelSortTime";
            labelSortTime.Size = new Size(166, 28);
            labelSortTime.TabIndex = 3;
            labelSortTime.Text = "Time to sort array";
            // 
            // button1
            // 
            button1.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button1.Location = new Point(477, 110);
            button1.Name = "button1";
            button1.Size = new Size(121, 56);
            button1.TabIndex = 4;
            button1.Text = "Run Test";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // textBoxUserInput
            // 
            textBoxUserInput.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            textBoxUserInput.Location = new Point(212, 121);
            textBoxUserInput.MaxLength = 6;
            textBoxUserInput.Name = "textBoxUserInput";
            textBoxUserInput.Size = new Size(179, 34);
            textBoxUserInput.TabIndex = 5;
            // 
            // progressBarBuildTime
            // 
            progressBarBuildTime.ForeColor = Color.Red;
            progressBarBuildTime.Location = new Point(473, 184);
            progressBarBuildTime.Name = "progressBarBuildTime";
            progressBarBuildTime.Size = new Size(125, 29);
            progressBarBuildTime.Step = 1;
            progressBarBuildTime.Style = ProgressBarStyle.Continuous;
            progressBarBuildTime.TabIndex = 6;
            // 
            // progressBarSortTime
            // 
            progressBarSortTime.ForeColor = Color.Blue;
            progressBarSortTime.Location = new Point(473, 212);
            progressBarSortTime.Name = "progressBarSortTime";
            progressBarSortTime.Size = new Size(125, 29);
            progressBarSortTime.TabIndex = 7;
            // 
            // FormPerformanceTest
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(814, 281);
            Controls.Add(progressBarSortTime);
            Controls.Add(progressBarBuildTime);
            Controls.Add(textBoxUserInput);
            Controls.Add(button1);
            Controls.Add(labelSortTime);
            Controls.Add(labelBuildTime);
            Controls.Add(labelDirections);
            Name = "FormPerformanceTest";
            Text = "Form1";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private Label labelDirections;
        private Label labelBuildTime;
        private Label labelSortTime;
        private Button button1;
        private TextBox textBoxUserInput;
        private ProgressBar progressBarBuildTime;
        private ProgressBar progressBarSortTime;
    }
}
