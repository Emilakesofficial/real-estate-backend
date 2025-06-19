from datetime import timezone
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Property
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.permissions import IsAdminUser
from django.db.models import Q

class PropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user if request.user.is_authenticated else None

        # Admins see everything; normal users see only active + published properties
        if user and user.is_staff:
            properties = Property.objects.all()
        else:
            properties = Property.objects.filter(is_active=True, is_published=True)

        # --- Filtering based on query parameters ---
        category = request.query_params.get('category')
        country = request.query_params.get('country')
        state = request.query_params.get('state')
        location = request.query_params.get('location')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search = request.query_params.get('search')

        # Clean and apply filters
        if category:
            category = category.strip()
            properties = properties.filter(property_type=category)
        if country:
            country = country.strip()
            properties = properties.filter(country__iexact=country)
        if state:
            state = state.strip()
            properties = properties.filter(state__iexact=state)
        if location:
            location = location.strip()
            properties = properties.filter(location__icontains=location)

        try:
            if min_price:
                properties = properties.filter(price__gte=float(min_price))
        except ValueError:
            pass  # Ignore invalid price filter

        try:
            if max_price:
                properties = properties.filter(price__lte=float(max_price))
        except ValueError:
            pass

        if search:
            search = search.strip()
            properties = properties.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        serializer = PropertySerializer(properties, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyPropertiesView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user

        if not hasattr(user, 'profile') or user.profile.role != 'agent':
            return Response({'detail': 'Only agents can view their properties.'}, status=status.HTTP_403_FORBIDDEN)
    
        properties = Property.objects.filter(agent=user, is_active=True).order_by('-created_at')
        serializer = PropertySerializer(properties, many=True, context={'request': request})
        return Response({'properties': serializer.data}, status=status.HTTP_200_OK)

class MyPropertyDetailView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request, pk):
        try:
            property = Property.objects.get(pk=pk, agent=request.user, is_active=True)
        except Property.DoesNotExist:
            return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(property, context={'request': request})
        return Response({'property': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Only agents can post properties
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'agent':
            return Response({'detail': 'Only agents can post properties.'}, status=status.HTTP_403_FORBIDDEN)

        # Proceed with serializer
        serializer = PropertySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Property created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message': 'Property creation failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        property = get_object_or_404(Property, pk=pk)

        if property.agent != request.user:
            return Response({'detail': 'You can only update your own properties.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PropertySerializer(property, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Property updated.', 'property': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        property = get_object_or_404(Property, pk=pk)

        if property.agent != request.user:
            return Response({'detail': 'You can only delete your own properties.'}, status=status.HTTP_403_FORBIDDEN)

        # Soft delete
        property.is_active = False
        property.is_published = False
        property.save()

        return Response({'message': 'Property deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class AdminPropertyView(APIView):
    
    permission_classes = [IsAuthenticated, IsAdminUser]
    # Restore
    def patch(self, request, pk):
        property = get_object_or_404(Property, pk=pk)

        if property.is_active:
            return Response({'detail': 'Property is already active.'}, status=status.HTTP_400_BAD_REQUEST)

        property.is_active = True
        property.is_published = True
        property.save()

        return Response({'message': 'Property restored successfully.'}, status=status.HTTP_200_OK)
    
    # Delete
    def delete(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        property.delete()
        return Response({'message': 'Property permanently deleted from the database.'}, status=status.HTTP_204_NO_CONTENT)

class MakeEnquiryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, property_id):
        user = request.user
        profile = getattr(user, 'profile', None)

        if not profile or profile.role.lower() not in ['renter', 'buyer', 'renter/buyer']:
            return Response({'detail': 'Only renters or buyers can make enquiries.'}, status=status.HTTP_403_FORBIDDEN)

        property = get_object_or_404(Property, id=property_id, is_active=True, is_published=True)

        serializer = EnquirySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            enquiry = serializer.save(user=user, property=property)

            # Send email to the agent
            send_mail(
                subject=f"New Enquiry on {property.title}",
                message=(
                    f"Hi {property.agent.first_name},\n\n"
                    f"You have received a new enquiry from {user.first_name} {user.last_name} "
                    f"({user.email}) regarding your property '{property.title}'.\n\n"
                    f"Message:\n{enquiry.message}\n\n"
                    f"Please log in to your dashboard to reply.\n\n"
                    f"Best regards,\nReal Estate Team"
                ),
                from_email=None,
                recipient_list=[property.agent.email],
                fail_silently=True,
            )

            return Response({'message': 'Enquiry submitted successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EnquiryReplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, enquiry_id):
        user = request.user
        profile = getattr(user, 'profile', None)
        if not profile or profile.role != 'agent':
            return Response({'detail': 'Only agents can reply to enquiries.'}, status=status.HTTP_403_FORBIDDEN)

        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        # Ensure the agent owns the property
        if enquiry.property.agent != user:
            return Response({'detail': 'You are not authorized to reply to this enquiry.'}, status=status.HTTP_403_FORBIDDEN)

        reply_text = request.data.get('reply')
        if not reply_text:
            return Response({'detail': 'Reply message is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the reply
        enquiry.reply = reply_text
        enquiry.replied_at = timezone.now()
        enquiry.save()

        # Notify the user via email
        send_mail(
            subject=f"Reply to your enquiry on {enquiry.property.title}",
            message=f"Hello {enquiry.user.first_name},\n\nYou received a reply to your enquiry on '{enquiry.property.title}':\n\n"
                    f"{reply_text}\n\nBest regards,\nReal Estate Team",
            from_email=None,
            recipient_list=[enquiry.user.email],
            fail_silently=True
        )

        return Response({'message': 'Reply sent and saved successfully.'}, status=status.HTTP_200_OK)

class AgentEnquiriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ensure only agents can access this
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'agent':
            return Response({'detail': 'Only agents can view enquiries.'}, status=status.HTTP_403_FORBIDDEN)

        # Fetch all enquiries for properties owned by this agent (i.e. where agent == request.user)
        enquiries = Enquiry.objects.filter(property__agent=request.user).order_by('-created_at')
        serializer = EnquirySerializer(enquiries, many=True, context={'request': request})
        return Response({'enquiries': serializer.data}, status=status.HTTP_200_OK)

class UserEnquiriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)

        if not profile or profile.role.lower() not in ['renter/buyer', 'renter', 'buyer']:
            return Response({'detail': 'Only renters or buyers can view their enquiries.'}, status=status.HTTP_403_FORBIDDEN)

        enquiries = Enquiry.objects.filter(user=user).order_by('-created_at')
        serializer = EnquirySerializer(enquiries, many=True, context={'request': request})
        return Response({'enquiries': serializer.data}, status=status.HTTP_200_OK)
