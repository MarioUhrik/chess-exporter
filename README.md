# chess-exporter
**Prometheus exporter for [chess.com](https://www.chess.com) player data implemented via [chess.com's published data API](https://www.chess.com/news/view/published-data-api) and [Prometheus Python Client](https://github.com/prometheus/client_python)**

Example use cases:
- Track [chess.com](https://www.chess.com) player ratings (and more) in your own [Prometheus](https://github.com/prometheus/prometheus) database
- Set up an [Alertmanager](https://github.com/prometheus/alertmanager) alert for when someone goes above 3000 rating in rapid on [chess.com](https://www.chess.com)
- Create a [Grafana](https://github.com/grafana/grafana) dashboard for conveniently viewing chess data of your favourite players on [chess.com](https://www.chess.com)

### Available metrics

Metric name | description | values |
--- | --- | --- |
chess_rapid_rating_current{playerName="playerName"} | Current chess.com rating of player *playerName* in rapid | integer |
chess_rapid_wins{playerName="playerName"} | Total number of wins of player *playerName* in rapid | integer |
chess_rapid_losses{playerName="playerName"} | Total number of losses of player *playerName* in rapid | integer |
chess_rapid_draws{playerName="playerName"} | Total number of draws of player *playerName* in rapid | integer |
chess_blitz_rating_current{playerName="playerName"} | Current chess.com rating of player *playerName* in blitz | integer |
chess_blitz_wins{playerName="playerName"} | Total number of wins of player *playerName* in blitz | integer |
chess_blitz_losses{playerName="playerName"} | Total number of losses of player *playerName* in blitz | integer |
chess_blitz_draws{playerName="playerName"} | Total number of draws of player *playerName* in blitz | integer |
chess_bullet_rating_current{playerName="playerName"} | Current chess.com rating of player *playerName* in bullet | integer |
chess_bullet_wins{playerName="playerName"} | Total number of wins of player *playerName* in bullet | integer |
chess_bullet_losses{playerName="playerName"} | Total number of losses of player *playerName* in bullet | integer |
chess_bullet_draws{playerName="playerName"} | Total number of draws of player *playerName* in bullet | integer |
chess_online{chess_online="online",playerName="playerName"} | online status of player *playerName*, **currently not working** | 0 or 1 |
chess_online{chess_online="offline",playerName="playerName"} | online status of player *playerName*, **currently not working** | 0 or 1 |
chess_online{chess_online="unknown",playerName="playerName"} | online status of player *playerName*, **currently not working** | 0 or 1 |

### Configuration

Chess-exporter is highly configurable via environment variables, and a configuration file.
- The [configuration file](https://github.com/MarioUhrik/chess-exporter/blob/main/manifests/conf/config.yaml) controls which metrics to track, and for which players
- The [environment variables](https://github.com/MarioUhrik/chess-exporter/blob/main/manifests/deployment.yaml) control a set of particular backend settings which you probably won't need to modify

---

Inspired by https://trstringer.com/quick-and-easy-prometheus-exporter/
