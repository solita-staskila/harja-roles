import pandas as pd
import matplotlib.pyplot as plt


def add_progress_bar_with_text(value, percentage):
    """
    Lisää progress barin taulukon columniin

    Parameters : 
        [int] value 
        [float] percentage 


    Returns:
        [str] html elementti
    """

    bar_width = min(max(percentage, 0), 100)

    return f'<div class="progress-container">' \
        f'<div class="progress-bar" style="width: {bar_width}%;"></div>' \
        f'<div class="progress-text">{value}</div>' \
        f'</div>'


def generate_role_table(df, columns, total, roles_count):
    """ 
    TODO 

    Parameters : 
        [df] df 
        [str] title
        [str] substr
        [arr] col
        [int] count


    Return: 
        [str] TODO 
    """

    formatted_v = f"{total:,}".replace(",", " ")
    formatted_r = f"{roles_count:,}".replace(",", " ")

    html_title = f"""
    <div style='display: flex; gap: 0px; flex-direction: column; align-items: flex-start; padding-bottom: 15px; max-width: 1400px; margin: auto;'>
        <div>Yhteensä rooleja: {formatted_r}</div>
        <div>Käyttäjiä rooleissa yhteensä: {formatted_v}</div>
        <div> </div>
    </div>
    """

    html_table = html_title + df[columns].to_html(escape=False)
    return html_table


def generate_header(tilanne, title="Report Title", date="dd/mm/yyyy"):

    logo_path = "logo_black.png"
    logo_html = f'<meta charset="UTF-8"><img src="resources/{logo_path}" alt="Logo" style="height: 35px; width: auto; margin-right: 10px;"/>'

    left_content = f"""
    <div style="float: left; width: 30%; text-align: left; padding-top: 6px">
        {logo_html}
    </div>
    """

    right_content = f"""
    <div style="float: right; width: 70%; max-width: 550px; text-align: right; font-size: 14px;">
        <div style="display: flex; justify-content: space-between;">
            <div style="float: left; text-align: left;">
                <p><strong>Tilanne:</strong> {tilanne}</p>
                <p><strong>Urakkatyypit:</strong> </p>
                
            </div>
            <div style="float: right; text-align: left;">
                <p><strong>Roolit:</strong> </p>
            </div>
        </div>
    </div>
    """

    title_content = f"""
    <div style="line-height: 0.5; clear: both; text-align: center; padding-top: 40px; padding-bottom: 35px;">
        <h1 style="font-size: 30px; font-weight: bold;">{title}</h1>
        <p style="color: grey; font-size: 14px;">{date}</p>
    </div>
    """

    header_html = f"""
    <div style="width: 100%; margin: auto; max-width: 1400px; height: 2px; background: black; margin-bottom: 16px;"></div>
    <div style="margin: auto; width: 90%; max-width: 1400px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        {left_content}
        {right_content}
    </div>
    {title_content}
    """
    return header_html


def generate_footer():

    logo_path = "logo_black.png"
    logo_html = f'<meta charset="UTF-8"><img src="resources/{logo_path}" alt="Logo" style="height: 35px; width: auto; margin-right: 10px;"/>'

    right_content = f"""
    <div style="float: right; width: 30%; text-align: right; padding-top: 6px">
        {logo_html}
    </div>
    """

    left_content = f"""
    <div style="float: left; width: 70%; max-width: 550px; text-align: right; font-size: 14px;">
        <div style="display: flex;">
            <div style="float: left; text-align: right;">
            
            </div>
            <div style="float: left; text-align: right;">
                <p>harja.palaute@solita.fi</p>
                <p></p>
                <p></p>
            </div>
        </div>
    </div>
    """

    footer = f"""
    <div style="width: 100%; margin: auto; max-width: 1400px; height: 2px; background: black; margin-bottom: 14px;"></div>
    <div style="margin: auto; width: 90%; max-width: 1400px; display: flex; justify-content: space-between; align-items: center;">
        {left_content}
        {right_content}
    </div>
    """
    return footer


def generate_matplotlib_piechart(df, filename, title, assigned, empty):
    """
    TODO 

    Parameters : 
        [df] df 
        [filename] filename 

    Returns: 
        TODO 
    """

    labels = df['tyyppi']
    sizes = df['count']

    formatted_e = f"{empty:,}".replace(",", " ")
    formatted_a = f"{assigned:,}".replace(",", " ")

    title_font = {'fontsize': 10, 'fontweight': 'bold', 'family': 'serif'}
    label_font = {'fontsize': 6, 'family': 'sans-serif'}
    autopct_font = {'fontsize': 5, 'family': 'monospace'}

    _, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: f'{p:.1f}%',
        startangle=90,
        textprops=label_font,
        colors=['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD']
    )

    ax.set_title(str(title + ' (' + formatted_a + ' / ' + formatted_e + ')'), title_font)

    for text in ax.texts:
        if '%' in text.get_text():
            text.set_fontsize(autopct_font['fontsize'])
            text.set_fontfamily(autopct_font['family'])

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()


def add_piechart(data, imgname, html, chart_title, assigned, empty):
    """  
    TODO 

    Parameters : 
        [arr] data 
        [str] img 
        [str] html 
        [str] title
        [str] chart title


    Returns: 
        TODO 
    """

    df = pd.DataFrame(data, columns=["tyyppi", "count", "prosentti"])
    generate_matplotlib_piechart(df, f'resources/{imgname}.png', chart_title, assigned, empty)

    html += f'<div style="padding-top:70px; max-width: 800px; margin: auto; width: 100%;  position: relative;">'
    html += f'<img src="resources/{imgname}.png" alt="none" style="width: 100%; margin-top: 24px; padding-bottom: 70px;">'
    html += f'</div>'

    return html


def piechart(roles_dict, imgname, html, chart_title):
    """  
    Lisää piechartin TODO 

    Parameters : 
        [dict] data 
        [str] img 
        [str] html 
        [str] title

    Returns: 
        TODO 
    """

    empty_count = 0
    total_assigned = 0

    for role_key, users in roles_dict.items():
        if len(users) == 0:
            empty_count += 1
        else:
            total_assigned += len(users)

    df = pd.DataFrame([
        ["Assignattu", total_assigned, 0],
        ["Tyhjät roolit", empty_count, 0]
    ], columns=["item", "count", "prosentti"])

    html = add_piechart(
        df.values,
        imgname,
        html,
        chart_title,
        total_assigned,
        empty_count
    )
    return html
