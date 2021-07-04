from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


def get_reports(token):
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(
        url="https://kitsu.io/api/graphql", headers={"Authorization": "Bearer " + token}
    )

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
      query Reports {
        reports(first: 10) {
          nodes {
            id
            explanation
            reason
            status
            updatedAt

            reporter {
              ...User
            }
            moderator {
              ...User
            }

            naughty {
              __typename
              ... on Comment {
                id
                author {
                  ...User
                }
                content
              }
              ... on Post {
                id
                author {
                  ...User
                }
                postMedia: media {
                  ...Media
                }
              }
              ... on MediaReaction {
                id
                author {
                  ...User
                }
                content: reaction
                media {
                  ...Media
                }
              }
            }
          }
        }
      }

      fragment Media on Media {
        titles {
          canonical
        }
        posterImage {
          original {
            url
          }
        }
      }

      fragment User on Profile {
        id
        name
        slug
        url
        avatarImage {
          original {
            url
          }
        }
      }
    """
    )

    # Execute the query on the transport
    return client.execute(query)
