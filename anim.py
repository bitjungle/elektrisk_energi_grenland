import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Configuration and Constants
ANIMATION_TITLE = 'Forbruk av elektrisk energi for industribedrifter i Porsgrunn og Bamble (blå søyler) \nsammenliknet med totalforbruk (all næring, privat og kommunal forbruk) i utvalgte kommuner (grønne søyler) \nog noen framtidige forbrukere i Porsgrunn og Skien (røde søyler)'
COPYRIGHT_NOTICE = 'Creative Commons BY-SA : Rune Mathisen (2024)'
DATA_SOURCE_NOTICE = 'Hoveddatakilde: Miljødirektoratet (Norske utslipp) og SSB'
MUSIC_COPYRIGHT_NOTICE = 'Musikk: lesfm-22579021 (Pixabay License)'
TODAYS_DATE = f'Animasjon laget den {datetime.date.today()}'

# Animation settings
TOTAL_DURATION = 75  # seconds for the main animation
HOLD_DURATION = 5    # seconds to hold the last frame
FPS = 50             # frames per second
FIG_SCALE = 4        # Scale factor for the figure size

# Output settings
OUTPUT_FOLDER = 'anim'
OUTPUT_FILE = 'anim.mp4'

# Data source settings
DATA_FOLDER = 'data'
DATA_FILE = 'el-forbruk.xlsx'
#DATA_SHEET = 'liste-over-forbrukere'
DATA_SHEET = 'forbrukere-og-kommuner'
DATA_COL_NAME = 'Bedrift'
DATA_COL_ENERGY = 'MWh'
DATA_COL_YEAR = 'år'
DATA_COL_COLOR = 'farge'

def read_and_prepare_data(file_path, sheet_name, header, sortcol):
    """
    Read and sort data from an Excel file.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet in the Excel file.
        header (int): Row (0-indexed) to use as the header.
        sortcol (str): Column to use for sorting.

    Returns:
        pandas.DataFrame: Sorted DataFrame.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header)
    return df.sort_values(by=sortcol, ascending=True)

def animate(frame_num, ax, df, total_frames):
    """
    Animation function to update the plot.

    Args:
        frame_num (int): Current frame number.
        ax (matplotlib.axes.Axes): The axes object to draw the animation.
        df (pandas.DataFrame): Data for animation.
        total_frames (int): Total number of frames in the main animation.
    """
    ax.clear()  # Clear previous drawings
    elapsed_time = frame_num / FPS
    if frame_num > total_frames:
        frame_num = total_frames

    ax.set_xlabel(DATA_COL_ENERGY, fontsize=12)
    ax.set_title(ANIMATION_TITLE, fontsize=14)

    bar_lengths = []
    for i, val in enumerate(df[DATA_COL_ENERGY]):
        start_time = (TOTAL_DURATION / len(df)) * i

        if elapsed_time >= start_time:
            growth_time = elapsed_time - start_time
            growth_duration = TOTAL_DURATION / len(df)
            growth_phase = min(growth_time / growth_duration, 1)
            bar_lengths.append(val * growth_phase)
        else:
            bar_lengths.append(0)

    ax.barh(df[DATA_COL_NAME], bar_lengths, color=df[DATA_COL_COLOR])
    current_max = max(bar_lengths) if bar_lengths else 0
    ax.set_xlim(0, current_max * 1.1)
    ax.set_ylim(-1, len(df))

    plt.text(0.5, 0.12, COPYRIGHT_NOTICE, ha='center', va='center', transform=ax.transAxes, fontsize=10, color='silver')
    plt.text(0.5, 0.10, DATA_SOURCE_NOTICE, ha='center', va='center', transform=ax.transAxes, fontsize=10, color='silver')
    plt.text(0.5, 0.06, MUSIC_COPYRIGHT_NOTICE, ha='center', va='center', transform=ax.transAxes, fontsize=8, color='silver')
    plt.text(0.5, 0.04, TODAYS_DATE, ha='center', va='center', transform=ax.transAxes, fontsize=8, color='silver')

def create_and_save_animation(df, duration, hold, fps, output_file):
    """
    Creates and saves the animation.

    Args:
        df (pandas.DataFrame): Data for animation.
    """
    fig, ax = plt.subplots(figsize=(FIG_SCALE*4, FIG_SCALE*3))
    total_frames = duration * fps
    hold_frames = hold * fps
    total_frames_with_hold = total_frames + hold_frames

    ani = animation.FuncAnimation(fig, lambda frame: animate(frame, ax, df, total_frames),
                                  frames=total_frames_with_hold, interval=1000/fps, repeat=False)

    ani.save(output_file, writer='ffmpeg', fps=fps)
    print(output_file)

if __name__ == "__main__":
    df_sorted = read_and_prepare_data(f'{DATA_FOLDER}/{DATA_FILE}', DATA_SHEET, 0, DATA_COL_ENERGY)
    print('Data read from Excel file:')
    print(df_sorted)
    create_and_save_animation(df_sorted, TOTAL_DURATION, HOLD_DURATION, FPS, f'{OUTPUT_FOLDER}/{OUTPUT_FILE}')
