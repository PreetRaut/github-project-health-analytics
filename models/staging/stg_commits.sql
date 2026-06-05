select

    sha,

    author_name,

    cast(author_date as timestamp) as author_date,

    message

from raw_commits