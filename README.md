# TM30-explanation
SUPERUSER CREDENTIALS
username = anthony
password = oreoluwa

CART/ ENDPOINT:
  The get method retrieves data of a user that is logged in and pending cart items. if no user is logged in it returns a permission denied error.
  The post method create new cart item to a logged in user. if the item exists in the store the values of that item is updated. else new cart item instance is created
  if the quantity demanded is greater the quantity in the store an error message response is sent
  
ITEMS/ ENDPOINT:
  The get method retrieves data of items that the quantity is more than 0. if no user is logged in it returns a permission denied error.
  The post method create new items if the authenticated user is an admin. denies access to non-staff users and anonymous users.
  
SINGLE-ITEM/<ITEM_ID>/ ENDPOINT:
  The get_item method gets an item from the database if the item exist. return an error message if item does not exist
  The get method retrieves an item from the Item model. endpoint is accessible by logged users if the request is a get method and admin users can perform the other methods
  The put method allows only the admin user to edit a sinlge item object to update the entire item or partial part of the data
  The delete method allows only the admin user to delete a single item object from the data
  
CART-ITEM-DELETE/ ENDPOINT:
  The delete method deletes a single cart item related to a user...
  The method is accessible to admin users and non-staff users
  
 DELIVER-ITEM/<CART_ID>/ ENDPOINT:
  The get method allow only admin users to change cart items order status to delivered.
  The method automatically deletes the delivered cart item provided the cart_id is given
  if the cart_item provided status is == delivered an error message is give {cart item not found}
  
    I wanted to add a user order history but it wasnt called for in the instructions and there was little time left.
    the model  gets the cart item deleted and stores the data of that cart item to the user order history model
  
  CARTVIEW:
    the cart serializer requires for only the cart_item id and quantity.
    the remaining data to be added to the view is automatically added (user_id that is logged using request.user.id, total_cost, status, date_ordered)
    
 SETTINGS:
  the setting has been splitted into three stages
  base, production, development to help me use settings that suit my working location
  base contains all common settings like install_apps, middleware etc
  development contains setting that all of base settings and settings i will need during development of my code e.g debug , allowed host, debub_toolbar
  
  Requirements.txt are the name implies is all that contains all of my project dependencies
  
  user activation token and id is gotten on the terminal
  
  permissions codes were written by me
   
    
    
