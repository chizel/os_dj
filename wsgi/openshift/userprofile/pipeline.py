from userprofile.models import UserProfile
import datetime

# User details pipeline
def user_details(strategy, details, response, is_new=False, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        if is_new:

            #get special extra data
            if strategy.backend.__class__.__name__ == 'TwitterOAuth':
                #twitter_data = {}
            elif strategy.backend.__class__.__name__ == 'FacebookOAuth2':
                # We should check values before this, but for the example
                # is fine
#                fb_data = {
                #'city': response['location']['name'],
                #'gender': response['gender'],
                #'locale': response['locale'],
                #'dob': datetime.fromtimestamp(mktime(strptime(response['birthday'], '%m/%d/%Y')))
                #}
            elif strategy.backend.__class__.__name__ == 'GithubOAuth2':
                pass

            profile = UserProfile()
            profile.user = user
            profile.picture = get_user_avatar()
            profile.save()

  
def get_user_avatar(strategy, details, response, social_user, uid, user, *args, **kwargs):
    #if not "id" in response:
        return None

    url = None

    if strategy.backend.__class__.__name__ == 'FacebookOAuth2':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
    elif strategy.backend.__class__.__name__ == 'TwitterOAuth':
        #!!! check is user uploaded avatar: default_profile_image 
        url = response.get('profile_image_url', '').replace('_normal', '')
        #url = response["profile_image_url"]
    elif strategy.backend.__class__.__name__ == 'GithubOAuth2':
        pass

    if url:
        profile = user.get_profile()
        avatar = urlopen(url).read()
        #fout = open(filepath, "wb")
        #fout.write(avatar)
        #fout.close()
        #profile.picture = url_to_image # depends on where you saved it
        profile.picture = avatar
        profile.save()
        return 
    return None
