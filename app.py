import os
import traceback
import asyncio
from coupons import Scrapper
from pytz import timezone 
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S")
logger = logging.getLogger(__name__)
page = 1
scp = Scrapper()

async def updater():
	global page, coup, current_time, count, html_code
	try:
		current_time = datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M:%S GMT%z %d-%m-%Y')
		logger.info("--------------Started collecting Coupons---------------------------------")
		links = []
		dis = await scp.discudemy(page)
		links.extend(dis)
		freebies = await scp.udemy_freebies(page)
		links.extend(freebies)
		tut = await scp.tutorialbar(page)
		links.extend(tut)
		coursev = await scp.coursevania(page)
		links.extend(coursev)
		coupon = await scp.idcoupons(page)
		links.extend(coupon)
		coup=""
		count=0
		for link in links:
			for lin in link:
				coup += f"{lin}<br>"
				count+=1
		logger.info(f"--------------successfully-collected---{count} coupons----------")
		html_code = f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8">
<link rel="apple-touch-icon" sizes="180x180" href="https://www.udemy.com/staticx/udemy/images/v7/apple-touch-icon.png" />
<link rel="icon" type="image/png" sizes="32x32" href="https://www.udemy.com/staticx/udemy/images/v8/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="https://www.udemy.com/staticx/udemy/images/v8/favicon-16x16.png" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>Udemy Coupons</title>
</head>
<u><center><h1> Latest Udemy Coupons ({count})</h1></center></u>
<center><h4> Updated at:- {current_time} </h4></center>
<body class="udemy-coupons" style="background-image:url('https://i.ibb.co/0KDVN8R/a7ef9e07d6ecbe6d7a9d2.webp');">
<ol type="1">
<!--coupons start--> 
{coup}  
<!--coupons end-->	
</ol>
</body>
<footer>
<center>
<p>Coded & Managed by: <a href ="https://github.com/adarsh-goel/" target=_blank > Adarsh Goel</a></p>
<p><a href="https://github.com/adarsh-goel/fresh-udemy-coupons" target=_blank >Give a star to the project🌟</a></p>
</center>
</footer>
</html>"""
		with open("index.html", "w+") as file:
			file.write(html_code)
	except TimeoutError:
		logger.info("Couldn't Collect Coupons..!")
	except Exception:
            	traceback.print_exc()
	return


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(updater())
