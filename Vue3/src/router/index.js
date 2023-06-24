import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '../views/Home.vue'
import DataManagement from '../components/DataManagement.vue'
import DataProcessing from '../components/DataProcessing.vue'
import Crawl from '../components/Crawl.vue'
import Query from '../components/Query.vue'
import News from '../components/News.vue'
import Search from '../components/Search.vue'
import VisualInterface from '../components/VisualInterface.vue'

// 数据处理
import AutoCrawl from '../components/DataProcessing/AutoCrawl.vue'
import Label from '../components/DataProcessing/Label.vue'
import DataUpload from '../components/DataProcessing/DataUpload.vue'
import Fusion from '../components/DataProcessing/Fusion.vue'
import LabelPage from '../components/DataProcessing/Label/LabelPage.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/DataManagement', component: DataManagement },
    { path: '/Crawl', component: Crawl },
    { path: '/Query', component: Query },
    { path: '/News', component: News },
    { path: '/Search', component: Search },
    { path: '/VisualInterface', component: VisualInterface },
    {
        path: '/DataProcessing',
        component: DataProcessing,
        children: [
            { path: '/DataProcessing/Label/:id', component: Label },
            { path: '/DataProcessing/DataUpload/:id', component: DataUpload },
            { path: '/DataProcessing/Fusion/:id', component: Fusion },
          
        ]
   
    },
    // 数据处理

]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

export default router