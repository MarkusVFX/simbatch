'''   created by: SimNode_01   [2019-02-25 21:26:36]   '''

import sys
sys.path.append("C:/mqs/git/simbatch")
import simbatch.core.core as simbatch_core
import simbatch.server.executor as executor

simbatch = simbatch_core.SimBatch("executor")
sibe = executor.SimBatchExecutor(simbatch, 2, 38)
interactions = sibe.batch.dfn.current_interactions
sibe.add_to_log_with_new_line( "START: id:38  evo:  descr:[13s]         tes t 22 fr")
interactions.maya_open_scene("C:\\exampleProj\\maya_proj\\FX\\copy\\base_setup\\copy_v003.mb")
interactions.maya_import_ani("C:\\exampleProj\\maya_proj\\ani\\123\\2\\")

interactions.maya_simulate_ncloth("1", "22", "nClothShape1", "C:\\exampleProj\\maya_proj\\FX\\copy\\123\\2\\cache\\cache_v002zzz_evo_www")
interactions.maya_save_scene("C:\\exampleProj\\maya_proj\\FX\\copy\\123\\2\\shot_setup\\copy__v001zzz_evo_www.mb")
interactions.maya_render_blast("1", "22", "C:\\exampleProj\\maya_proj\\FX\\copy\\123\\2\\prev\\copy__prev__v001zzz_evo_www\\copy__prev__v001zzz_evo_www__####.jpg")


sibe.finalize_queue_job()
