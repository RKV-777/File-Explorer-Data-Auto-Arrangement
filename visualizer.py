import os
import logging
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
from fileopsbot import root_directory


class FileLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(message)s'
        )

    def log_file_data(self, filename, filesize, extn, creation_date):
        logging.debug(f"{filename},{filesize},{extn},{creation_date}")


class FileProcessor:
    def __init__(self, root_directory, log_file):
        self.root_directory = root_directory
        self.log_file = log_file

    def process_files(self):
        logger = FileLogger(self.log_file)
        for filename in os.listdir(self.root_directory):
            file_path = os.path.join(self.root_directory, filename)
            if os.path.isfile(file_path):  
                ext = os.path.splitext(filename)[1]  
                filesize = os.path.getsize(file_path) 
                creation_date = time.ctime(os.path.getctime(file_path)) 
                logger.log_file_data(filename, filesize, ext, creation_date)

    def read_logs(self):
        df = pd.read_csv(self.log_file, header=None)
        df.columns = ['Filename', 'Size', 'ext', 'Date']
        return df

    def summarize_files(self, df):
        summary = df.groupby('ext').agg(
            size=('Size', 'sum'),
            count=('ext', 'count')
        ).sort_values(by='size', ascending=False).reset_index()
        return summary
    
    def fileage(self,df):
        age_summary = df.groupby(['ext', 'Date']).size().reset_index(name='count')
        age_summary = age_summary.sort_values(by='Date').reset_index(drop=True)
        return age_summary


class FileVisualizer:
    @staticmethod
    def pie_chart(summary):
        labels = summary['ext']
        sizes = summary['size']
        colors = [
            "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])
            for _ in range(len(sizes))
        ]
        max_value = max(sizes)
        max_index = sizes.tolist().index(max_value)
        explode = [0.1 if i == max_index else 0 for i in range(len(sizes))]

        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True)
        plt.title("File Size Distribution by Extension")
        plt.show()



if __name__ == "__main__":

    log_file = "FileLogs.csv"

    processor = FileProcessor(root_directory, log_file)
    processor.process_files()

    df = processor.read_logs()

    summary = processor.summarize_files(df)
    age_sum=processor.fileage(df)

    visualizer = FileVisualizer()
    visualizer.pie_chart(summary)