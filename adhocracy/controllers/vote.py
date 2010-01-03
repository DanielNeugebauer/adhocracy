from pylons.i18n import _

from adhocracy.lib.base import *
from adhocracy.model.forms import VoteCastForm

log = logging.getLogger(__name__)

class VoteController(BaseController):
    
    @RequireInstance
    @RequireInternalRequest()
    @validate(schema=VoteCastForm(), form="cast_error", post_only=False, on_get=True)
    def cast(self, id):
        c.motion = get_entity_or_abort(model.Motion, id)
        if not c.motion: 
            abort(404, _("No motion with ID %(id)s exists.") % {'id': id})
        if not h.has_permission("vote.cast"):
            h.flash(_("You have no voting rights."))
            redirect_to("/motion/%s" % str(id))  
        if not c.motion.poll:
            h.flash(_("This motion is not currently being voted on.")) 
            redirect_to("/motion/%s" % str(id))
            
        orientation = self.form_result.get("orientation")
        votes = democracy.Decision(c.user, c.motion.poll).make(orientation)
        for vote in votes:
            event.emit(event.T_VOTE_CAST, vote.user, scopes=[c.instance], 
                       topics=[c.motion, vote.user], vote=vote, poll=c.motion.poll)
        redirect_to("/motion/%s" % str(id))
        
    def cast_error(self, id):
        h.flash(_("Illegal input for vote cast."))
        redirect_to("/motion/%s" % str(id))
