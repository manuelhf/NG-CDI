import tkinter as tk
from tkinter import filedialog, ttk
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap, BoundaryNorm

import os
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.spatial.distance import hamming
import re
from PIL import Image, ImageTk

############# PACKAGE VERSIONS ##############
# import tkinter as tk
# print("tkinter:", tk.Tk().eval('info patchlevel'))

# # Seaborn
# import seaborn as sns
# print("seaborn:", sns.__version__)

# # Matplotlib
# import matplotlib
# print("matplotlib:", matplotlib.__version__)

# # OS, RE, and scipy don't have versions as they are part of the Python standard library or utilities.

# # Numpy
# import numpy as np
# print("numpy:", np.__version__)

# # Pandas
# import pandas as pd
# print("pandas:", pd.__version__)

# # Scipy
# import scipy
# print("scipy:", scipy.__version__)

# # PIL (known as Pillow)
# from PIL import Image
# print("Pillow (PIL):", Image.__version__)


########## ACTUAL CODE ####################

class AnomalyDetectorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main UI elements
        self.title("NGCDI Anomaly Detector")
        self.geometry("1200x800")
        
        # Create the status label at the top left
        self.status_label = tk.Label(self, text="Select Options", font=("Arial", 14, "bold"))
        self.status_label.pack(anchor=tk.W, padx=5)


        # # Upload Excel button
        # self.upload_button = tk.Button(self, text="Upload Excel", command=self.upload_excel)
        # self.upload_button.pack(pady=5)

        # # Dropdown menu for selecting traffic type
        # self.link_var_traffic = tk.StringVar()
        # self.dropdown = ttk.Combobox(self, textvariable=self.link_var_traffic, values=[
        #     'peaktime', 'noon'
        # ])
        # self.dropdown.pack(padx=5)
        
        # self.link_var = tk.StringVar()
        # self.dropdown = ttk.Combobox(self, textvariable=self.link_var, values=[
        #     'A1 - B1', 'A1 - B2', 'A1 - B3', 'A1 - C1', 'A1 - C2', 'A1 - C4',
        #     'A1 - C6', 'A1 - C7', 'A1 - C8', 'B1 - B2', 'B1 - B3', 'B1 - C2',
        #     'B1 - C3', 'B1 - C7', 'B1 - C8', 'B2 - B3', 'B2 - B4', 'B2 - C3',
        #     'B2 - C4', 'B2 - C5', 'B2 - C6', 'B3 - C2', 'B3 - C4', 'B3 - C5',
        #     'B3 - C8', 'B4 - C2', 'B4 - C7', 'C7 - C8'
        # ])
        # self.dropdown.pack(pady=5)
        
        # Create a container frame for the three widgets
        container_frame = tk.Frame(self)
        container_frame.pack(pady=5)
        
        # Upload Excel button
        self.upload_button = tk.Button(container_frame, text="Upload Excel", command=self.upload_excel)
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        # Dropdown menu for selecting traffic type
        self.link_var_traffic = tk.StringVar()
        self.link_var_traffic.set("Select Traffic Type")
        self.dropdown_traffic = ttk.Combobox(container_frame, textvariable=self.link_var_traffic, values=['peaktime', 'noon'])
        self.dropdown_traffic.pack(side=tk.LEFT, padx=5)
        
        # Dropdown menu for selecting links
        self.link_var = tk.StringVar()
        self.link_var.set("Select Route")
        self.dropdown_links = ttk.Combobox(container_frame, textvariable=self.link_var, values=[
            'A1 - B1', 'A1 - B2', 'A1 - B3', 'A1 - C1', 'A1 - C2', 'A1 - C4',
            'A1 - C6', 'A1 - C7', 'A1 - C8', 'B1 - B2', 'B1 - B3', 'B1 - C2',
            'B1 - C3', 'B1 - C7', 'B1 - C8', 'B2 - B3', 'B2 - B4', 'B2 - C3',
            'B2 - C4', 'B2 - C5', 'B2 - C6', 'B3 - C2', 'B3 - C4', 'B3 - C5',
            'B3 - C8', 'B4 - C2', 'B4 - C7', 'C7 - C8'
        ])
        self.dropdown_links.pack(side=tk.LEFT, padx=5)
        
        
        
        
        # Dropdown menu for selecting route type
        self.link_var_route = tk.StringVar()
        self.link_var_route.set("Select Direction")
        self.dropdown_route = ttk.Combobox(container_frame, textvariable=self.link_var_route, values=['A->Z', 'Z->A'])
        self.dropdown_route.pack(side=tk.LEFT, padx=5)
        
        
        

        # Detect Anomaly button
        self.detect_button = tk.Button(self, text="Analyze Link", command=self.detect_anomaly)
        self.detect_button.pack(pady=5)

        # Placeholder for plots
        self.canvas = None
        self.image_labels = []

        # Data store
        self.df = None
        self.canvas_width = 550  # Example width
        self.canvas_height = 350  # Example height
        
        
        # Create frames for canvases
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Create canvases
        self.canvas1 = tk.Canvas(left_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas1.pack(pady=5)
        
        self.canvas2 = tk.Canvas(left_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas2.pack(pady=5)
        
        self.canvas3 = tk.Canvas(right_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas3.pack(pady=5)
        

    def upload_excel(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.csv")])
        if filepath:
            self.df = pd.read_csv(filepath, header=1)
            mask_noon = (self.df['Measure'] == 'noon') & (self.df['Direction'] == 'A->Z')
            routes = self.df[mask_noon]['Route'].unique()
            # Extract terms enclosed within single quotes and treat them as single terms
            unique_routes = set()
            for route in routes:
                terms = re.findall(r"'(.*?)'", route)
                unique_routes.update(terms)
            # self.dropdown["values"] = list(unique_routes)



    def display_on_canvas(self, image_path, canvas):
        """
        Display an image on a given canvas.

        Parameters:
        - image_path (str): Path to the image file.
        - canvas (tk.Canvas): The canvas on which to display the image.
        """
        # Open and resize the image to fit the canvas dimensions
        image = Image.open(image_path)
        image = image.resize((self.canvas_width, self.canvas_height), Image.ANTIALIAS)
        
        # Convert the Image object to a PhotoImage object for use in Tkinter
        photo_image = ImageTk.PhotoImage(image)
        
        # Store the reference to the photo_image to prevent garbage collection issues
        canvas.image = photo_image
        
        # Display the image
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)





    def detect_anomaly(self):
        
        self.status_label.config(text="Working on it...", fg="red")
        self.update_idletasks()
        
        match_term = self.link_var.get()
        
        signal = self.link_var_traffic.get()
        
        direction = self.link_var_route.get()

        print(signal)
        
        
        ########## SPECIFY LINK TYPE - EXPERIMENTAL####
                                                   #<------------------change link pattern here
        
        
        mask_peak_select = (self.df['Measure'] == signal) & (self.df['Direction'] == direction) & (self.df['Route'].str.contains(match_term))
        df_filtered_peak_select = self.df.loc[mask_peak_select]
        df_extracted_peak_select = df_filtered_peak_select.iloc[:, 3:447]
        
        # mask_peak_select = (self.df['Measure'] == 'peaktime') & (self.df['Direction'] == 'A->Z') & (self.df['Route'].str.contains(match_term))
        # df_filtered_peak_select = self.df.loc[mask_peak_select]
        # df_extracted_peak_select = df_filtered_peak_select.iloc[:, 3:447]
        
        
        # mask_noon_select = (self.df['Measure'] == 'noon') & (self.df['Direction'] == 'A->Z') & (self.df['Route'].str.contains(match_term))
        # df_filtered_noon_select = self.df.loc[mask_noon_select]
        # df_extracted_noon_select = df_filtered_noon_select.iloc[:, 3:447]
        
        
        peak_select = df_extracted_peak_select
        # noon_select = df_extracted_noon_select
        
        
        
        ###### MATRIX PROFILE #################
        
        
        
        
        def convert_to_SAX(time_series, alphabet_size_1=4, alphabet_size_2=4):
            """
            Convert a Z-normalized time series to its SAX representation, considering two alphabet sizes.
            
            Parameters:
            - time_series (array): The Z-normalized time series data.
            - alphabet_size_1 (int): The size of the SAX alphabet for the first two values.
            - alphabet_size_2 (int): The size of the SAX alphabet for the next five values.
            
            Returns:
            - sax_repr (string): The SAX representation of the time series.
            """
            # Define the SAX alphabet
            alphabet_1 = "abcdefghijklmnopqrstuvwxyz"[:alphabet_size_1]
            alphabet_2 = "abcdefghijklmnopqrstuvwxyz"[:alphabet_size_2]
            
            # Compute the breakpoints based on the Gaussian distribution
            breakpoints_1 = norm.ppf(np.linspace(1./alphabet_size_1, 1-1./alphabet_size_1, alphabet_size_1-1))
            breakpoints_2 = norm.ppf(np.linspace(1./alphabet_size_2, 1-1./alphabet_size_2, alphabet_size_2-1))
            
            # Convert the time series to its SAX representation
            sax_repr = ''
            for idx, val in enumerate(time_series):
                if idx < 2:  # First two values
                    alphabet = alphabet_1
                    breakpoints = breakpoints_1
                else:  # Next five values
                    alphabet = alphabet_2
                    breakpoints = breakpoints_2
                
                sax_symbol = alphabet[0]  # Default to the first symbol
                for i, bp in enumerate(breakpoints):
                    if val < bp:
                        break
                    sax_symbol = alphabet[i+1]
                sax_repr += sax_symbol
                
            print(sax_repr)
            
            return sax_repr
        
        
        
        
        def calculate_matrix_profile_sax(sax_repr, m):
            """
            Calculate the matrix profile for a SAX representation of a time series with subsequence length `m`,
            using Hamming distance as the distance metric.
            
            Parameters:
            - sax_repr (string): The SAX representation of the time series.
            - m (int): The length of the subsequence.
            
            Returns:
            - matrix_profile (array): The matrix profile of the SAX representation.
            """
            
            N = len(sax_repr)
            matrix_profile = np.zeros(N - m + 1)
            matrix_profile.fill(float('inf'))
            
            for i in range(0, N - m + 1):
                subseq_i = sax_repr[i:i+m]
                
                for j in range(i+1, N - m + 1):
                    subseq_j = sax_repr[j:j+m]
                    dist = hamming(list(subseq_i), list(subseq_j))
                    
                    if dist < matrix_profile[i]:
                        matrix_profile[i] = dist
                    if dist < matrix_profile[j]:
                        matrix_profile[j] = dist
                        
            return matrix_profile
        
        
        
        
        def plot_sax_representation(y, sax_repr, alphabet_size_1=4, alphabet_size_2=4):
            """
            Plot the original time series and overlay the SAX representation using color-coded bars.
            
            Parameters:
            - y (list): Original time series.
            - sax_repr (string): SAX representation of the time series.
            - alphabet_size_1 (int): The size of the SAX alphabet for the first two values.
            - alphabet_size_2 (int): The size of the SAX alphabet for the next five values.
            """
            
            # Generate a unique color map for each alphabet letter
            alphabet_1 = "abcdefghijklmnopqrstuvwxyz"[:alphabet_size_1]
            alphabet_2 = "abcdefghijklmnopqrstuvwxyz"[:alphabet_size_2]
            colors_1 = plt.cm.viridis(np.linspace(0, 1, alphabet_size_1))
            colors_2 = plt.cm.plasma(np.linspace(0, 1, alphabet_size_2))
            color_map = dict(zip(alphabet_1, colors_1))
            color_map.update(dict(zip(alphabet_2, colors_2)))
        
            plt.figure(figsize=(20, 6))
            plt.plot(y, label='Original Time Series', color='blue')
            
            # Overlay the SAX representation using color-coded bars
            for idx, letter in enumerate(sax_repr):
                plt.axvspan(idx, idx + 1, color=color_map[letter], alpha=0.4, label=f'SAX: {letter}')
                
             # Set x-ticks to appear every 7th reading
            tick_positions = list(range(0, len(y), 7))
            tick_labels = [str(i//7) for i in tick_positions]
            plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=90)
            
            # Avoid duplicate labels in the legend
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())
            
            plt.title('Original Time Series with Overlayed SAX Representation')
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.grid(True)
            plt.savefig('p3.png', dpi=200)
            plt.show()
        
        ########## CHECK THROUGH THE SIGNAL LINKS ##########
        
        
        
        detection_store=[]
        
        
        for i in range(0,peak_select.shape[0]):
        
            # Regenerate the sample time series data
            y = peak_select.iloc[i,:]                       #<------------------------- change peak/noon
            
            # Z-normalize the time series
            mean_y = np.mean(y)
            std_y = np.std(y)
            y_normalized = (y - mean_y) / std_y
            
            
            num_days = 435
            # Define the subsequence length (m)
            m = 7
            
            plt.figure(figsize=(20, 6))
            # plt.plot(y[range_start:range_stop], label="Timeseries signal")
            plt.plot(y, label="Timeseries signal")
            plt.xlabel("Days")
            plt.ylabel("Distance")
            plt.title(f"Timeseries {match_term}")
            # Set x-ticks to appear every 7th tick
            tick_positions = np.arange(0, num_days, 7)  # 101 because you're plotting 101 points from index 200 to 300
            tick_labels = [str(i // 7) for i in tick_positions]
            plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=90)
            plt.grid()
            plt.show()
            
            
            
        
            
            # Convert the Z-normalized time series to its SAX representation
            sax_repr = convert_to_SAX(y_normalized)
            
                
            # Calculate the matrix profile for the SAX representation with subsequence length m=7
            matrix_profile_sax = calculate_matrix_profile_sax(sax_repr, m)
            detection_store.append(matrix_profile_sax)
            
            
            xticks_positions = np.arange(0, num_days, 7)  # every 7th day
            xticks_labels = [str(i // 7) for i in xticks_positions]  # week numbers
        
            
            # Plot the matrix profile for the SAX representation
            plt.figure(figsize=(25, 4))
            plt.plot(matrix_profile_sax, label="Matrix Profile (SAX, Hamming Distance)")
            plt.xlabel("Week")
            plt.ylabel("Distance")
            plt.title(f"Matrix Profile with Subsequence Length {m} (SAX, Hamming Distance) for {match_term}")
            plt.xticks(ticks=xticks_positions, labels=xticks_labels, rotation=90)
            plt.grid(True)
            plt.show()
            
            
            
            
            plot_sax_representation(y, sax_repr)
            
            
            
            # Find indices where matrix_profile_sax > 0.15
            indices_to_plot = np.where(matrix_profile_sax > 0.15)[0]
            indices_to_plot = np.sort(indices_to_plot)  # Sort the indices for easier processing
            
            # Cluster indices that are within 40 data points of each other
            clusters = []
            current_cluster = []
            prev_idx = -1
            
            for idx in indices_to_plot:
                if prev_idx == -1 or idx - prev_idx <= 40:
                    current_cluster.append(idx)
                else:
                    clusters.append(current_cluster)
                    current_cluster = [idx]
                prev_idx = idx
            
            if current_cluster:
                clusters.append(current_cluster)
            
            
        
        
            
            # Loop through clusters and plot segments
            for cluster in clusters:
                # Determine the start and stop indices for plotting
                range_start = max(0, cluster[0] - 10)
                range_stop = min(len(y), cluster[-1] + 10)
            
                plt.figure(figsize=(15, 6))
                plt.plot(y[range_start:range_stop], label="Timeseries signal")
            
                for idx in cluster:
                    plot_idx = idx - range_start  # Adjust the index relative to the segment being plotted
                    plt.axvline(x=plot_idx, color='r', linestyle='--', label=f'Matrix Profile > 0.15 at {idx}')
            
                plt.xlabel("Days")
                plt.ylabel("Distance")
                plt.title(f"Timeseries {match_term} for clustered indices")
            
                # Set x-ticks to appear every 2nd tick
                tick_positions = list(range(0, range_stop - range_start + 1, 2))
                tick_labels = [str(i) for i in range(range_start, range_stop + 1, 2)]
                plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=90)
            
                # Show legend but avoid duplicate labels
                # handles, labels = plt.gca().get_legend_handles_labels()
                # by_label = dict(zip(labels, handles))
                # plt.legend(by_label.values(), by_label.keys())
            
                plt.show()
        
        
        
        
        
        ################# TESTING SEVERITY #####################
        
        def get_classified_indices(matrix_profile_sax):
            """
            Classify the values in the matrix profile based on thresholds and return the indices of each classification.
            
            Parameters:
            - matrix_profile_sax (list): List of matrix profile values.
            
            Returns:
            - classified_indices (dict): Dictionary with classifications as keys and list of indices as values.
            """
            
            classified_indices = {
                "average": [],
                "high": [],
                "severe": [],
                "out_of_bounds": []
            }
            
            for idx, value in enumerate(matrix_profile_sax):
                if 0 <= value < 0.15:
                    classified_indices["average"].append(idx)
                elif 0.15 <= value < 0.3:
                    classified_indices["high"].append(idx)
                elif 0.3 <= value < 0.5:
                    classified_indices["severe"].append(idx)
                else:
                    classified_indices["out_of_bounds"].append(idx)
            
            return classified_indices
        
        
        
        def plot_time_series_with_classifications(y, matrix_profile_sax):
            """
            Plot the original time series and mark the classified locations from the matrix profile.
            
            Parameters:
            - y (list): Original time series.
            - matrix_profile_sax (list): List of matrix profile values.
            """
            
            classifications = get_classified_indices(matrix_profile_sax)
            
            plt.figure(figsize=(20, 6))
            plt.plot(y, label='Original Time Series', color='blue')
            
            # Use scatter for better legends
            plt.scatter(classifications["average"], [y[idx] for idx in classifications["average"]],
                        color='green', label='Average')
            plt.scatter(classifications["high"], [y[idx] for idx in classifications["high"]],
                        color='yellow', label='High')
            plt.scatter(classifications["severe"], [y[idx] for idx in classifications["severe"]],
                        color='red', label='Severe')
            
            plt.title(f'Severity Plot for for {match_term}')
            plt.xlabel('Weeks')
            plt.ylabel('Bandwidth usage')
            
            # Set x-ticks to appear every 7th reading
            tick_positions = list(range(0, len(y), 7))
            tick_labels = [str(i//7) for i in tick_positions]
            plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=90)
            
            
            plt.legend()
            plt.grid(True)
            plt.savefig('p1.png', dpi=200)
            plt.show()
        
        
        # Test the plotting function
        # Generate a synthetic y for demonstration purposes
        
        plot_time_series_with_classifications(y, matrix_profile_sax)
        
        
        
        ################### PLOTTING UNIQUE SIGNATURES ###################
        
        def plot_sax_trends_updated(y, sax_repr, m):
            """
            Plot the average trend for each unique SAX alphabet based on the segments of the time series they represent.
            
            Parameters:
            - y (list): Original time series.
            - sax_repr (string): SAX representation of the time series.
            - m (int): Subsequence length used for the SAX representation.
            """
            
            unique_sax_letters = set(sax_repr)
            plt.figure(figsize=(8, 5))
            
            for letter in unique_sax_letters:
                indices = [i for i, x in enumerate(sax_repr) if x == letter]
                
                # Extract segments of the time series corresponding to the current SAX letter
                segments = [y[idx:idx+m] for idx in indices if len(y[idx:idx+m]) == m]
                
                # Calculate the average trend for this SAX letter
                avg_segment = np.mean(segments, axis=0)
                
                plt.plot(avg_segment, label=f'SAX: {letter}')
            
            plt.title(f'Average Trend for Each Unique SAX Letter for {match_term}')
            plt.xlabel('Days of week')
            plt.ylabel('BW amplitude')
            plt.legend()
            plt.grid(True)
            plt.savefig('p2.png', dpi=100)
            plt.show()
        
        # Re-run the demonstration
        plot_sax_trends_updated(y, sax_repr, 7)
        
        self.status_label.config(text="Done", fg="green")
        
        self.display_on_canvas("p1.png", self.canvas1)
        self.display_on_canvas("p2.png", self.canvas2)
        self.display_on_canvas("p3.png", self.canvas3)


if __name__ == "__main__":
    app = AnomalyDetectorApp()
    app.mainloop()
