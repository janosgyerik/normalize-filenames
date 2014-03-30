import re

re_well_formatted = re.compile(r'([A-Z0-9]\w* )+\(\d{4}\)\.[a-z][a-z0-9]{2}$')
re_split_to_parts = re.compile(r'(.*\w).*(\d{4}).*\.(...)$')
re_split_to_parts_noyear = re.compile(r'(.*\w).*\.(...)$')
re_split_to_parts_noext = re.compile(r'(.*\w).*(\d{4}).*$')
re_split_to_parts_noyear_noext = re.compile(r'(.*\w)')


class MovieFilenameNormalizer(object):
    def is_well_formatted(self, filename):
        return re_well_formatted.match(filename)

    def normalize(self, filename):
        if self.is_well_formatted(filename):
            return filename
        basename, year, ext = self.split_to_parts(filename)
        n_basename = self.normalize_basename(basename)
        n_ext = self.normalize_ext(ext)
        if year:
            return '%s (%s).%s', n_basename, year, n_ext
        return '%s.%s', n_basename, n_ext

    def split_to_parts(self, filename):
        match = re_split_to_parts.match(filename)
        if match:
            return match.groups()
        match = re_split_to_parts_noyear.match(filename)
        if match:
            basename, ext = match.groups()
            return basename, None, ext
        match = re_split_to_parts_noext.match(filename)
        if match:
            basename, year = match.groups()
            return basename, year, None
        return filename, None, None

    def normalize_basename(self, basename):
        return basename.strip().title()

    def normalize_ext(self, ext):
        return ext.lower()
