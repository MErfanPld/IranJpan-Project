from django.urls import translate_url
from django.conf import settings
from .forms import SearchForm


def search_form(request):
    return {
        'search_form': SearchForm(request.GET or None)
    }


def redirect_to(request):
    """
    Provide a language-switch friendly 'next' URL.
    Uses full path (path + query string) so language switch preserves
    the current page and any query parameters.
    Django's set_language view will translate the URL to the target language.
    """
    return {'redirect_to': request.get_full_path()}


def language_alternates(request):
    """
    Build absolute alternate language URLs for hreflang / SEO.
    Returns a list of dicts: [{'code': 'fa', 'url': 'https://...'}, ...]
    """
    current_path = request.path
    alternates = []
    for lang_code, _ in settings.LANGUAGES:
        try:
            translated = translate_url(current_path, lang_code)
            if translated:
                url = request.build_absolute_uri(translated)
            else:
                # fallback: simple prefix replace
                parts = current_path.strip('/').split('/')
                if parts and parts[0] in dict(settings.LANGUAGES):
                    parts[0] = lang_code
                    new_path = '/' + '/'.join(parts) + ('/' if current_path.endswith('/') else '')
                else:
                    new_path = f'/{lang_code}{current_path}'
                url = request.build_absolute_uri(new_path)
            alternates.append({'code': lang_code, 'url': url})
        except Exception:
            continue
    return {'language_alternates': alternates}
