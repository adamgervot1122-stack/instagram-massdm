"""All agents are registered here."""

from ..types import AgentName
from .competitor import CompetitorAgent
from .content_engine import ContentEngineAgent
from .landing_page import LandingPageAgent
from .market_score import MarketScoreAgent
from .offer_generator import OfferGeneratorAgent
from .ppc import PPCAgent
from .reddit_pain import RedditPainAgent
from .seo_hunter import SEOHunterAgent
from .social_viral import SocialViralAgent
from .trend_hunter import TrendHunterAgent

REGISTRY = {
    AgentName.trend_hunter: TrendHunterAgent,
    AgentName.seo_hunter: SEOHunterAgent,
    AgentName.reddit_pain: RedditPainAgent,
    AgentName.social_viral: SocialViralAgent,
    AgentName.competitor: CompetitorAgent,
    AgentName.offer_generator: OfferGeneratorAgent,
    AgentName.landing_page: LandingPageAgent,
    AgentName.ppc: PPCAgent,
    AgentName.content_engine: ContentEngineAgent,
    AgentName.market_score: MarketScoreAgent,
}

__all__ = ["REGISTRY"]
