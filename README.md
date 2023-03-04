# Price-Tracking-App
#### Overview ::
This python scripted app is built with keeping the intention of scrapping some e-commerce websites and providing instant information about the price drop of the product. Currently, it is functional in local devices and works perfectly fine for ***Flipkart*** products. But in the future, this project aims to expand overall e-commerce websites. Here I have built a simple website with  ***Flask*** for the user interface. Let's dive deep into the insights then...
# Login / Create account ::
This is the entrance of the website, accomodating all the user interactions. If new to the website, then the user has to create one first. And If not they can directly enter by filling up the login form.

![loginsignin](https://user-images.githubusercontent.com/56407204/124709112-bee7bf00-df18-11eb-982c-df7e10a11253.jpg)

# Home page ::
The user will enter this page as soon as they log in. Here basically, the basic instruction about using the website is mentioned. I recommend reading it before exploring the website.

![home](https://user-images.githubusercontent.com/56407204/124710493-7cbf7d00-df1a-11eb-8500-c24f902bb373.PNG)

# Add Url ::
This page is meant for adding URLs, and the price upper bound depending on which user wants to notify himself through the app. Adding any invalid email would not be accepted. The valid URL requests which are given here get reflected in the ***My Url List*** section.

![add](https://user-images.githubusercontent.com/56407204/124710746-cf009e00-df1a-11eb-9120-e922717f6bcf.PNG)

# My Url list ::
This page shows all the requests of URLS filled by the user. Cancellation option is also available. Once the price goes beyond the upper bound, the product automatically gets deleted from the list, and the email gets sent to the user right away.

![my list](https://user-images.githubusercontent.com/56407204/124711168-5ea64c80-df1b-11eb-8c8d-f2e0267b4f98.PNG)

# The price tracking script::
This part comprises the python file ***app2.py*** . Here I am going through the entire database where all the URL request of each user is stored. Then using the BeautifulSoup lib, I'm parsing the HTML page of the corresponding product page in Flipkart. From here, I'm searching for the ***div*** tag with ***class :: " _30jeq3 _16Jk6d "***. Below I have shown why that particular attribute of the div tag is being used to get the product's price. 


And whenever the price goes beyond the price upper bound, the user gets a notification by registered email with the help of the ***Send Mail*** function. The corresponding product gets deleted from the database using the ***Cancel*** function. 
Finally, this entire process is carried out inside a loop with a precise time gap (currently 30 sec) 

![finall](https://user-images.githubusercontent.com/56407204/124713385-1a687b80-df1e-11eb-8e7a-0860fb0fa775.PNG)


