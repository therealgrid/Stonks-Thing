import os
import csv
import pygame
from tkinter import Tk, filedialog

# Function to clean up stock market data from a CSV file
def clean_csv(input_file, output_folder):
    filename = os.path.basename(input_file)
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        cleaned_data = [row for row in reader if len(row) == 6]  # Assuming data has 6 columns
    with open(os.path.join(output_folder, filename), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])  # Header
        writer.writerows(cleaned_data)

# Function to display a window using Pygame
def main():
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((400, 200))
    pygame.display.set_caption('Stock Data Cleaner')

    font = pygame.font.SysFont(None, 30)
    text = font.render('Select CSV File', True, (0, 0, 0))
    text_rect = text.get_rect(center=(200, 100))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    Tk().withdraw()
                    input_file = filedialog.askopenfilename(title='Select CSV File', filetypes=[("CSV files", "*.csv")])
                    output_folder = 'cleaned_data'  # You can change this to your desired output folder
                    if input_file:
                        clean_csv(input_file, output_folder)
                        print("CSV file cleaned successfully!")
                        running = False

        window.fill((255, 255, 255))
        window.blit(text, text_rect)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()



