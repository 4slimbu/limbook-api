import os

from config import Config


class TestConfig(Config):
    # Test db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL', 'sqlite:///test.db?check_same_thread=False'
    )

    # Test Image directory
    IMG_UPLOAD_DIR = '/static/img/uploads/test'

    # Suppress mail sending
    MAIL_SUPPRESS_SEND = True

    """Invalid token generated by unknown source for testing."""
    EXAMPLE_INVALID_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ' \
                            '9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpv' \
                            'aG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwR' \
                            'JSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

    """Valid token generated by Auth0 but has expired."""
    EXAMPLE_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6' \
                    'IllhT3RnLWR4WmJMRmZOUnlOQkVEbSJ9.eyJpc3MiOiJodHRwcz' \
                    'ovL2xpbXZ1cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViN' \
                    'jZhMmQxY2MxYWMwYzE0OTZjMTZmIiwiYXVkIjoibGltYm9vay1' \
                    'hcGktYXV0aCIsImlhdCI6MTU5MDMzNDM2MiwiZXhwIjoxNTkwM' \
                    'zQxNTYyLCJhenAiOiIxcjhTc0o4SDJwbURyelh0RXJaQUMwTko' \
                    '4MFh3NkFGaiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY' \
                    '3JlYXRlOmNvbW1lbnRzIiwiY3JlYXRlOmltYWdlcyIsImNyZWF' \
                    '0ZTpwb3N0cyIsImNyZWF0ZTpyZWFjdHMiLCJkZWxldGU6Y29tb' \
                    'WVudHMiLCJkZWxldGU6aW1hZ2VzIiwiZGVsZXRlOnBvc3RzIiw' \
                    'iZGVsZXRlOnJlYWN0cyIsInJlYWQ6Y29tbWVudHMiLCJyZWFkO' \
                    'mltYWdlcyIsInJlYWQ6cG9zdHMiLCJyZWFkOnJlYWN0cyIsInV' \
                    'wZGF0ZTpjb21tZW50cyIsInVwZGF0ZTppbWFnZXMiLCJ1cGRhd' \
                    'GU6cG9zdHMiLCJ1cGRhdGU6cmVhY3RzIl19.Eg0yQYmmEjMVBQ' \
                    'KHgHH19llxwaYL_pUBvVWzb8YySv4VLYO8v64GIru_1yg2AYAc' \
                    'hY8LiqjxNjlIEfmlu4VIrkz37FL1WatKSo9SCD_Ej5mjsMeuR0' \
                    'RYINR_DdfZTo5U0BJpX6ShdENu6fTFQlC_kcI2g7zZbD6kS5HV' \
                    '9cj2G31crDhiX4s2oJEtrauuRVf0XQqQsDdfU0yvrP_gGX1F3Q' \
                    'sbXZtItUtJEb3jZw2QCSj5LoLsyx_N0oh29gTG_asj8us8iSb3' \
                    'qc3IGyPo6G4miEgLLMl2rD9hdKQ6UyKAWusFdfDmIeAhJbjeNG' \
                    'rMmVwPTXzLa8acDdOqb3OvFRonWQ'

    """ Valid token generated by Auth0 for user without any assigned role.

    This token has expired but can be used to check invalid permissions by
    bypassing token verification while testing.
    """
    NO_PERMISSION_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsI' \
                          'mtpZCI6IllhT3RnLWR4WmJMRmZOUnlOQkVEbSJ9.eyJp' \
                          'c3MiOiJodHRwczovL2xpbXZ1cy5hdXRoMC5jb20vIiwi' \
                          'c3ViIjoiYXV0aDB8NWVjYTk1OWU5MmRjZTgwYzZmMTc2' \
                          'ZDU4IiwiYXVkIjoibGltYm9vay1hcGktYXV0aCIsImlh' \
                          'dCI6MTU5MDMzNTAwOCwiZXhwIjoxNTkwMzQyMjA4LCJh' \
                          'enAiOiIxcjhTc0o4SDJwbURyelh0RXJaQUMwTko4MFh3' \
                          'NkFGaiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltd' \
                          'fQ.OFi1B5JkT-PZDq8I8OXojLg7bjyjRRNx0LUWpoVer' \
                          'VyHRh3G54QqMZ3e_c3GArij7KIW1Bup3XAnl8emHxbi6' \
                          'Bvkkvxs1EF_AGbGUED5mDFwUo2PtCGkncIpC2TsBkIRZ' \
                          'jOTLkFfWnoNXxsJnHVjgTacGwa65_D8oxNicAqeV-ZpC' \
                          '1jilvVre4563IpzfA-H_SEUuqblQI6Si4M7HNBIkag5g' \
                          'qqenma2o29BzN7dvNtHG67rR7pa8KgXehgrYLI46p8I0' \
                          'Rnz5evEb8pprwPZyz7zdZij58ARGju8qj_ZmlEhLVgpl' \
                          'Q14mYs1mBmD7uWNxllRk_a9yqkFCA5qN29nRg'

