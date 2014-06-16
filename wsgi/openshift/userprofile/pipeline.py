from userprofile.models import UserProfile
import datetime

# User details pipeline
def user_details(strategy, details, response, is_new=False, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        if is_new:
            attrs = {'user': user}

            if strategy.backend.__class__.__name__ == 'TwitterOAuth':
                #twitter_data = {}
                #attrs = dict(attrs.items() + twitter_data.items())

                #UserProfile.objects.create(
                    #**attrs
                #)

                profile = UserProfile()
                profile.user = user
                profile.save()
                return

            elif strategy.backend.__class__.__name__ == 'FacebookOAuth2':
                # We should check values before this, but for the example
                # is fine
#                fb_data = {
                #'city': response['location']['name'],
                #'gender': response['gender'],
                #'locale': response['locale'],
                #'dob': datetime.fromtimestamp(mktime(strptime(response['birthday'], '%m/%d/%Y')))
                #}
                #attrs = dict(attrs.items() + fb_data.items())
                #UserProfile.objects.create(
                #**attrs
                #)
                profile = UserProfile()
                profile.user = user
                profile.save()
            elif strategy.backend.__class__.__name__ == 'GithubOAuth2':
                profile = UserProfile()
                profile.user = user
                profile.save()

  
def get_user_avatar(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    elif backend.__class__ == TwitterBackend:
        #!!! check is user uploaded avatar: default_profile_image 
        url = response.get('profile_image_url', '').replace('_normal', '')

    if url:
        profile = user.get_profile()
        avatar = urlopen(url).read()
        fout = open(filepath, "wb")#filepath is where to save the image
        fout.write(avatar)
        fout.close()
        profile.photo = url_to_image # depends on where you saved it
        profile.save()
