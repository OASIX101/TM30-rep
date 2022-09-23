from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Cart, Item
from TM30_accounts.models import CustomUser 
from TM30_accounts.permissions import IsAdminOnly, IsUserAuthenticated, IsUserOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from .serializers import CartSerializer, ItemSerializer, ItemUserSerializer, CartReqSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied

class ItemView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrReadOnly]
    
    def get(self, request, format=None):
        """
        Allow logged in user and admin to get all items in the database.
        If item quantity is equal to zero it does not show in the retrieved data.
        It also returns the number of user that ordered the item.
        Allows only admin to post items.
        """
        obj = Item.objects.all()
        new_data = []
        for item in obj:
            if item.quantity_available > 0:
                new_data.append(item)

        serializer = ItemUserSerializer(new_data, many=True, )

        data = {
            'message': 'retrieve sucessful',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body=ItemSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
            
        serializer = ItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            data = {
                "message":"success"
            }

            return Response(data, status = status.HTTP_200_OK)

        else:
            data = {
                "message":"failed",
                "error":serializer.errors
            }
        
        return Response(data, status = status.HTTP_400_BAD_REQUEST)

class ItemsEditView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get_item(self, item_id):
        """
        Tries to retrieves an item from the database with the given id.
        If the item does not exist, it returns an error message.
        """
        
        try:
            return Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise NotFound(detail={'message': 'Item with id does not exist.'})

    def get(self, request, item_id, format=None):
        
        """
        Retrieve an item from the database with the given id
        Allows only 
           
        """
        obj = self.get_item(item_id=item_id)
        serializer = ItemSerializer(obj)

        data = {
            'message': 'Successful retrieve',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='put', request_body=ItemSerializer())
    @action(methods=['PUT'], detail=True)
    def put(self, request, item_id, format=None):
        """
        Updates the entire or partial data of an existing item in the database.
        Allows only admin users to update the given item.
        """

        obj = self.get_item(item_id=item_id)
        serializer = ItemSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {
                'message': 'update successful',
                'data': serializer.data
            }

            return Response(data, status=status.HTTP_202_ACCEPTED)

        else:

            data = {
                'message': 'update failed',
                'data': serializer.errors
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)
    def delete(self, request, item_id, format=None):

        """Deletes an existing item from the database.
           Returns a message response to be sure it deleted and a status code of 204 NO_CONTENT.
           It is only accessible to admin users.
        """

        obj = self.get_item(item_id=item_id)
        obj.delete()
        data = {
            'message': 'Item deleted successfully.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

class CartView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserAuthenticated]

    def get(self, request, format=None):
        """
        Retrieves a logged in user cart from the database, only pending items are shown.
        Anonymoususer are restricted from using this method.
        returns an error message if user is not logged in.
        """
        if request.user in CustomUser.objects.all():

            user_id = request.user.id
            object = CustomUser.objects.get(id=user_id)
            obj = object.user.filter(status='pending')

            serializer = CartSerializer(obj, many=True)

            data = {
                'message': 'cart retrieve successful',
                'total orders': obj.count(),
                'data': serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied(detail={'error': 'AnonymousUser not authorized and has no cart present in the database.'})

    @swagger_auto_schema(method='post', request_body=CartReqSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """
        Adds items to the cart of a user in the database to the cart model only if the  
        item quantity available in the database is greater than quantity demanded.
        Accessible only to logged in users.

        """  
        data = {}
        data['cart_item'] = request.data['cart_item']
        data['quantity'] = request.data['quantity']
        data['user'] = request.user.id
        try:
            catem = Item.objects.get(id=data['cart_item'])          
            catem_price = catem.price
            data['item_cost'] = data['quantity'] * catem_price
            data['status'] = 'pending'

            if request.user in CustomUser.objects.all():
                
                if data['quantity'] > catem.quantity_available:
                    return Response(data={'message': 'Quantity ordered is higher than quantity available in store'}, status=status.HTTP_403_FORBIDDEN)

                else:
                    catem.quantity_available -= data['quantity'] 
                    catem.save()
                    serializer = CartSerializer(data=data)
                    
                    if serializer.is_valid():
                        serializer.save()
                        
                        data = {
                            "message":"item successfully added to cart",
                        }

                        return Response(data, status = status.HTTP_200_OK)

                    else:
                        data = {
                            "message":"failed",
                            "error":serializer.errors
                        }
                    
                    return Response(data, status = status.HTTP_400_BAD_REQUEST)

            else:
                raise PermissionDenied(detail={'message': 'AnonymousUser are forbidden to perform this action.'})

        except Item.DoesNotExist:
            raise NotFound(detail={'message': 'Item with id does not exist'})

class CartEditView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserAuthenticated]

    def get_cart_item(self, cart_id):
        """
        Tries to retrieves a cart item from the database with the given id.
        If the cart does not exist, it returns an error message.
        """
        
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            raise NotFound(detail={'message': 'cart-item with id does not exist.'})
   

    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)
    def delete(self, request, cart_id, format=None):
        """Delete a single cart item relating to a logged in user.
           Returns a reponse message 'success' if deleted successfully and status code of 204.
           when a pending cart item is deleted the quantity is added to the quantity of the item model.
        """
        try:
            user_id = request.user.id
            object = CustomUser.objects.get(id=user_id)

            
            if request.user == object and request.user in CustomUser.objects.all():
                obj = self.get_cart_item(cart_id=cart_id)
                try: 
                    p = Item.objects.get(item_name=obj.cart_item)
                    p.quantity_available+=obj.quantity
                    p.save()
                
                    obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except Cart.DoesNotExist:
                    raise NotFound(detail={'message': 'Cart does not exist'})

            else:
                raise PermissionDenied(detail={'message': 'user is forbidden to acces another user data or user is anonymous.'})
            
        except CustomUser.DoesNotExist:
            raise NotFound(detail={'message': 'User is an anonyousUser.'})

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOnly])
def delivered_items(request, cart_id):
    """Allows admin user to change the status of a cart item to delivered if the item has been delivered to the user"""
    
    if request.method == 'GET':
        try:
            cart_item = Cart.objects.get(id=cart_id, status="pending")
            cart_item.status = "delivered"
            cart_item.save()
       
            return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error":"Cart not found","message":"failed"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOnly])
def make_pending(request, cart_id):
    """Allows admin user to make a cart item status to 'pending' if the item wasnt successfully delievered"""
    
    if request.method == 'GET':
        try:
            cart_item = Cart.objects.get(id=cart_id, status="delivered")
            cart_item.status = "pending"
            cart_item.save()
       
            return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error":"not found","message":"failed"}, status=status.HTTP_404_NOT_FOUND)