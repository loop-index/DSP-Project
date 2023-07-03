def convert_cost(cost):
    return 0.14 * cost * 0.1

def ad_html(advertiser, campaign, adText, width=300, height=250):
    return '''
    <style>
        /* CSS styles for the ad creative */
        .ad-container {{
            background-color: #F2F2F2;
            border: 2px solid #E4E4E4;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
            width: {width}px;
            height: {height}px;
        }}
        
        .advertiser {{
            font-size: 24px;
            color: #333333;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .campaign {{
            font-size: 24px;
            color: #666666;
            margin-bottom: 15px;
        }}
        
        .ad-text {{
            font-size: 32px;
            color: #555555;
        }}
    </style>
    <div class="ad-container">
        <div class="advertiser">{advertiser}</div>
        <div class="ad-text">{adText}</div>
        <div class="campaign">{campaign}</div>
    </div>
    '''.format(advertiser=advertiser, campaign=campaign, adText=adText, width=width, height=height)
