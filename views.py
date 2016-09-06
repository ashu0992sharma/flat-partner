import os
import urllib
import webbrowser
import json

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, renderers

from . import utils, models, serializers, constants

import json
import requests
import datetime
import re

class FlatShow(APIView):
    """"""

    def get(self, request):
        """

        :param request:
        :return:
        """
        r = requests.get('https://graph.facebook.com/v2.7/195366117186736/feed?'
                         'fields=id%2Cname%2Cfrom%2Cmessage%2Cupdated_time&access_token='
                         'EAACEdEose0cBAIAx79rtW3Qtn4yVw9NiH0ZAasqrrnUWZB3n6yZAIvB59Xgif'
                         'NUXrcEXRGaEIlyER6oUg7jLh93nbmwILy5v8rKMQBzfKGdhrbcjpANMkbnN4EeaiEmhJjuRrUk5Q6Vtb0BCHGBFpEfdy23X0y1lKfw5kRALwZDZD')
        return Response( {'response' : r.json()}, status=status.HTTP_200_OK)


class SearchApi(APIView):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        search_string = request.GET.get('search_string')
        date_diff = request.GET.get('date_diff')
        date_diff = int(date_diff) if date_diff else None
        furnishing_type = request.GET.get('furnished_type', ' ')
        furnishing_type = furnishing_type.strip() if furnishing_type else furnishing_type
        gender = request.GET.get('gender', '').strip()
        print gender
        search_string = search_string.strip().split("|")
        flat_ids = []
        for token in search_string:
            flat_ids.extend(utils.raw_search(token))

        query = {}
        if date_diff:
            query = {'publish_at__gte': datetime.timedelta(days=date_diff)}

        if furnishing_type:
            query['furnishing_type__icontains'] = furnishing_type

        if gender:
            query['gender__icontains'] = gender

        print query
        print flat_ids
        flats = (models.Flat.objects.filter(pk__in=flat_ids, **query).order_by('-publish_at'))
        serializer = serializers.FlatSerializer(flats, many=True)
        return Response({'response': serializer.data}, status=status.HTTP_200_OK)


class SaveFlatData(APIView):
    """

    """

    def get(self, request):
        """

        :param request:
        :return:
        """

        file_name = "mysite/flats_data.json"
        with open(file_name) as data_file:
            data = json.load(data_file)
            for datum in data:
                post_id = datum.get('id')
                user_id = datum.get("from").get("id")
                name = datum.get("from").get("name")
                message = datum.get("message", 'share a flat')
                updated_at = datum.get("updated_time")
                image = datum.get("picture")
                models.Flat.objects.create(user_fb_id=user_id, user_fb_name=name, message=message, publish_at=updated_at,
                                           image=image, post_id=post_id)

        return Response( {'response': 'success'}, status=status.HTTP_200_OK)


class ExtraData(APIView):
    """

    """

    def get(self, request):
        """
        :return:
        """

        flats_data = models.Flat.objects.all()
        for data in flats_data:
            post_id = data.id
            message = data.message
            try:
                numbers_list = re.findall(r'\d+', message)
                phone_number = [a for a in numbers_list if len(a) > 9 and len(a) < 12]
                phone_number = phone_number[0] if phone_number else None
                data.phone_number = phone_number
            except Exception as exc:
                print exc
            if 'furnished' in message:
                data.furnishing_type = 'furnished'
            else:
                data.furnishing_type = 'semi-furnished'
            data.save()

        return Response( {'response': 'success'})

class CheckAvailability(APIView):
    """

    """

    def get(self, request):
        """

        :param request:
        :return:
        """
        with open("mysite/195366117186736_comments.json") as data_file:
            data = json.load(data_file)
            for datum in data:
                closed_word_dict = constants.CLOSED_DICT
                comments = datum.get('comments')
                if comments:
                    for comment in comments.get('data'):
                        message  = comment.get('message')
                        if any(word in message for word in closed_word_dict):
                            if comment.get("from").get("id") == datum.get('from').get('id'):
                                print datum.get('id'), message
                                posts = models.Flat.objects.filter(post_id=datum.get('id'))
                                for post in posts:
                                    post.is_available = False
                                    post.save()
        return Response({'success':'success'}, status=status.HTTP_200_OK)


class SavePostLikes(APIView):
    """

    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        with open("mysite/195366117186736_likes.json") as data_file:
            data = json.load(data_file)
            for datum in data:
                posts = models.Flat.objects.filter(post_id=datum.get('id'))
                likes = int(datum.get('likes').get('summary').get('total_count'))
                for post in posts:
                    post.like_count = likes
                    post.save()
        return Response({'success': 'success'}, status=status.HTTP_200_OK)


class GetGender(APIView):
    """

    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        gender_list = constants.GENDER_LIST
        flat_ids = []
        for token in gender_list:
            flat_ids.extend(utils.raw_search(token))
        flats = models.Flat.objects.filter(pk__in=flat_ids)
        for flat in flats:
            flat.gender = models.Flat.GENDER_CHOICES[1][0]
            flat.save()

        return Response({'success': 'success'}, status=status.HTTP_200_OK)

class GetFlatData(APIView):
    """
    
    """

    def get(self, request):
        """
        """

        t = requests.get('https://graph.facebook.com/oauth/access_token?client_id=1481890605170164&client_secret=20a62b932a5ac8b84cff353a71e14f7c&grant_type=client_credentials')
        r = requests.get('https://graph.facebook.com/v2.7/838402552906457/feed?fields=id%2Cname%2Cfrom%2Cmessage%2Cupdated_time%2cpicture&' + t.text)
        d = r.json()
        with open('fixture/838402552906457.json', 'w') as outfile:
            json.dump(d["data"], outfile, indent=4, sort_keys=True, separators=(',', ':'))

        while (d["paging"]["next"]):

            r = requests.get(d["paging"]["next"])
            d = r.json()

            with open('fixture/838402552906457.json', 'a') as outfile:
                json.dump(d["data"], outfile, indent=4, sort_keys=True, separators=(',', ':'))

        return Response( {'response' : "hello"}, status=status.HTTP_200_OK)



class UserData(APIView):
    """
	"""

    def get(self, request,id):
		"""
		"""
		print (id)
		r = requests.get('https://graph.facebook.com/oauth/access_token?client_id=1481890605170164&client_secret=20a62b932a5ac8b84cff353a71e14f7c&grant_type=client_credentials')
		r = requests.get('https://graph.facebook.com/v2.7/' + str(id) + '?fields=name,id,email,picture&' + r.text)
		return Response( {'response' : r.json()}, status=status.HTTP_200_OK)


class CommentsData(APIView):
	"""
	"""

	def get(self, request):

            """
            """

            t = requests.get('https://graph.facebook.com/oauth/access_token?client_id=1481890605170164&client_secret=20a62b932a5ac8b84cff353a71e14f7c&grant_type=client_credentials')
            r = requests.get('https://graph.facebook.com/v2.7/838402552906457/feed?fields=id%2Cfrom%2Ccomments&' + t.text)
            d = r.json()
            with open('fixture/838402552906457_comments.json', 'w') as outfile:
                json.dump(d["data"], outfile, indent=4, sort_keys=True, separators=(',', ':'))

            while (d["paging"]["next"]):
                r = requests.get(d["paging"]["next"])
                d = r.json()
                with open('fixture/838402552906457_comments.json', 'a') as outfile:
                    json.dump(d["data"], outfile, indent=4, sort_keys=True, separators=(',', ':'))

            return Response( {'response' : "hello"}, status=status.HTTP_200_OK)

    #-----------------------------------------------------------------------------------------------------
class LikesData(APIView):
	"""
	"""

	def get(self, request):

            """
            """

            t = requests.get('https://graph.facebook.com/oauth/access_token?client_id=1481890605170164&client_secret=20a62b932a5ac8b84cff353a71e14f7c&grant_type=client_credentials')
            r = requests.get('https://graph.facebook.com/v2.7/838402552906457/feed?fields=likes.summary(true)&' + t.text)
            d = r.json()
            with open('fixture/838402552906457_likes.json', 'w') as outfile:
                json.dump(d["data"], outfile, indent=4, sort_keys=True, separators=(',', ':'))

            while (d["paging"]["next"]):
                r = requests.get(d["paging"]["next"])
                d = r.json()
                with open('fixture/838402552906457_likes.json', 'a') as outfile:
                    json.dump(d["data"], outfile, indent=4, sort_keys=True, separators=(',', ':'))

            return Response( {'response' : "hello"}, status=status.HTTP_200_OK)
