import html, json, os, re, sqlite3, time, urllib.request, urllib.parse, urllib.error

# Токен: аз муҳити системавӣ (BOT_TOKEN) гирифта мешавад, агар набошад — аз сатри поён
BOT_TOKEN = os.environ.get("BOT_TOKEN", "9294317208:AAHNHS_0x2nG4KWWxbP9SvPRO0o9aCu4k2o")

CHANNEL_ID = -1004335970973
CHANNEL_URL = "https://t.me/cpmssm"
BOT_USERNAME = "CPM_SSM_Gift_bot"
NEED = 5
ADMIN_ID = 8731580691
REVIEW_CHAT = ADMIN_ID          # отзывҳо ба куҷо меоянд: ADMIN_ID ё ID-и гурӯҳи админ
REVIEW_AUTOPUBLISH = False      # False = аввал админ тасдиқ мекунад; True = худкор ба канал
BUTTON_STYLES = True            # рангҳои тугмаҳо (сабз/сурх/кабуд), Bot API 9.4+
PAGE = 5                        # чанд аккаунт дар як саҳифаи архив

# --- Топ дня: ҳар рӯз 1 аккаунт ба лидер ---
TZ_OFFSET = 5 * 3600            # Тоҷикистон UTC+5
DAILY_MIN = 1                   # ҳадди ақал чанд даъват барои ғолиб шудан
ANNOUNCE_IN_CHANNEL = True      # эълон кардани ғолиб дар канал

BOT_VERSION = "v12-camps-upgrade"   # дар панели админ ва ҳангоми оғоз нишон дода мешавад

DEFAULT_LANG = "ru"

S = {
    "ru": {
        "welcome": (
            "👋 Привет!\n\n"
            "Хочешь получить подарок — полный аккаунт? 🎁\n\n"
            "Пригласи друзей в наш канал по своей личной ссылке:\n"
            "• {n1} человек — 1 аккаунт\n"
            "• {n2} человек — 2 аккаунта\n"
            "• {n3} человек — 3 аккаунта\n"
            "и так далее!\n\n"
            "🏆 Каждый день №1 по приглашениям получает +1 аккаунт в подарок!\n\n"
            "Аккаунт придёт автоматически, как только условие выполнено.\n\n"
            "Выбери действие ниже 👇"),
        "help": (
            "❓ Как это работает\n\n"
            "1️⃣ Нажми «Моя ссылка» — получишь личную ссылку на канал.\n"
            "2️⃣ Отправь её друзьям. Каждый, кто вступит по ней, засчитывается.\n"
            "3️⃣ За каждые {need} человек — 1 аккаунт. Он придёт сюда автоматически.\n"
            "4️⃣ Каждый день №1 по приглашениям получает +1 аккаунт.\n\n"
            "ℹ️ Если приглашённый выйдет из канала, он перестанет считаться.\n"
            "📦 Все полученные аккаунты всегда лежат в разделе «Мои аккаунты»."),
        "share_text": ("🎁 В канале CPM_SSM раздают полные аккаунты бесплатно!\n"
                       "Заходи по моей ссылке и забирай свой 👇"),
        "menu_title": ("🏠 Главное меню\n\n"
                       "👥 Приглашено: {c}   📦 Получено аккаунтов: {g}\n\n"
                       "Выбери действие 👇"),
        "btn_claim_n": "🎁 Забрать подарок ({n})",
        "btn_claim": "🎁 Забрать подарок",
        "btn_link": "🔗 Моя ссылка",
        "btn_getlink": "🔗 Получить ссылку",
        "btn_progress": "📊 Прогресс",
        "btn_top": "🏆 Топ",
        "btn_today": "📅 Топ дня",
        "btn_accounts": "📦 Мои аккаунты",
        "btn_help": "❓ Как это работает",
        "btn_channel": "📢 Перейти в канал",
        "btn_review": "📸 Оставить отзыв",
        "btn_lang": "🌐 Язык",
        "btn_back": "⬅️ Меню",
        "btn_home": "🏠 Меню",
        "btn_sub": "📢 Подписаться на канал",
        "btn_subbed": "✅ Я подписался",
        "btn_share": "📤 Поделиться ссылкой",
        "btn_ready": "📨 Готовое сообщение",
        "btn_send_friends": "📤 Отправить друзьям",
        "btn_retry": "🔄 Повторить",
        "btn_skip": "Пропустить",
        "btn_prev": "‹ Назад",
        "btn_next": "Вперёд ›",
        "st_left": "Осталось пригласить до следующего аккаунта: {n}",
        "st_total": "👥 Всего приглашено: {n}",
        "st_earned": "🏅 Заработано аккаунтов: {n}",
        "st_got": "📦 Уже получено: {n}",
        "st_avail": "🎁 Доступно к получению: {n}",
        "progress_title": "📊 Ваш прогресс:",
        "anon": "Участник",
        "unit": "чел.",
        "you": "← вы",
        "top_title": "🏆 Топ-10 по приглашениям",
        "top_empty": "🏆 Топ пока пуст. Станьте первым — пригласите друзей!",
        "top_place": "Ваше место: {p} ({n} чел.)",
        "top_none": "Вы пока никого не пригласили.",
        "today_title": "📅 Топ дня",
        "today_left": "⏳ До конца дня: {h} ч {m} мин",
        "today_prize": "🎁 Победитель получит +1 аккаунт (минимум {n} приглашённых)",
        "today_empty": "Сегодня пока никого. Ты можешь стать первым! 🚀",
        "today_place": "Ваше место сегодня: {p} ({n} чел.)",
        "today_none": "Сегодня вы ещё никого не пригласили.",
        "archive_empty": "📦 У вас пока нет полученных аккаунтов.",
        "archive_title": "📦 Ваши аккаунты ({t}) стр. {p}/{n}",
        "sub_prompt": "Сначала подпишитесь на наш канал, затем нажмите «Я подписался» 👇",
        "link_fail": "😔 Не удалось создать ссылку. Попробуйте чуть позже.",
        "link_text": ("🔗 Ваша личная ссылка:\n{link}\n\n"
                      "За каждые {need} приглашённых — 1 аккаунт.\n\n{status}"),
        "give_updated": "Некоторые приглашённые вышли из канала, счёт обновлён.\n\n",
        "give_empty": ("Аккаунты сейчас закончились, скоро добавим ⏳\n"
                       "Позже нажмите «Забрать подарок» ещё раз."),
        "gift": ("🎁 Ваш подарок:\n\n{data}\n\nСпасибо, что с нами! ❤️\n"
                 "📦 Все аккаунты всегда есть в разделе «Мои аккаунты»."),
        "giveaway_win": ("🎉 Поздравляем, вы победитель розыгрыша!\n\n"
                         "🎁 Ваш приз:\n\n{data}\n\nСпасибо, что с нами! ❤️"),
        "review_ask": ("📸 Оставь, пожалуйста, отзыв!\n\n"
                       "Отправь сюда скриншот из аккаунта — мы покажем его в канале, "
                       "чтобы друзья тоже захотели получить подарок.\n\n"
                       "⚠️ Только не показывай на скриншоте логин и пароль."),
        "review_ask_winner": ("🏆 Поздравляем, ты победитель!\n\n"
                              "Отправь, пожалуйста, скриншот из аккаунта — мы покажем его в канале "
                              "как отзыв победителя 🎉\n\n"
                              "⚠️ Только не показывай на скриншоте логин и пароль."),
        "review_thanks": "Спасибо за отзыв! ❤️ Он появится в канале после проверки.",
        "review_published": "🎉 Ваш отзыв опубликован в канале. Спасибо!",
        "review_hint": "Хотите оставить отзыв? Нажмите кнопку, затем отправьте скриншот 👇",
        "review_after_only": "Отзыв можно оставить после получения аккаунта 🎁",
        "new_member": "✅ Новый участник вступил по вашей ссылке!\n\n{status}",
        "congrats": "🎉 Поздравляем! Вы пригласили {c} человек!",
        "claim_need": "Пока приглашено {c}/{need}. Нужно ещё {r}.",
        "claim_all": ("Все доступные аккаунты уже получены. "
                      "Пригласите ещё {r} человек для следующего."),
        "daily_win": ("🏆 Вы — №1 по приглашениям за вчера ({c} чел.)!\n\n"
                      "🎁 Ваш подарок дня:\n\n{data}\n\nСпасибо, что с нами! ❤️"),
        "lang_prompt": "🌐 Выберите язык / Забонро интихоб кунед / Тилди тандаңыз",
        "invited": ("🎉 Вас пригласил(а) {who}!\n\n"
                    "В нашем канале раздают полные аккаунты бесплатно 🎁\n"
                    "Хотите тоже получить подарок? Нажмите кнопку ниже и получите свою ссылку 👇"),
    },
    "tg": {
        "welcome": (
            "👋 Салом!\n\n"
            "Мехоҳӣ тӯҳфа — аккаунти пурра — гирӣ? 🎁\n\n"
            "Дӯстонатро бо истиноди шахсии худ ба канали мо даъват кун:\n"
            "• {n1} нафар — 1 аккаунт\n"
            "• {n2} нафар — 2 аккаунт\n"
            "• {n3} нафар — 3 аккаунт\n"
            "ва ҳамин тавр идома!\n\n"
            "🏆 Ҳар рӯз №1 аз рӯи даъватҳо +1 аккаунт ҳамчун тӯҳфа мегирад!\n\n"
            "Аккаунт ҳамин ки шарт иҷро шуд, худкор меояд.\n\n"
            "Амалро дар поён интихоб кун 👇"),
        "help": (
            "❓ Чӣ тавр кор мекунад\n\n"
            "1️⃣ «Истиноди ман»-ро пахш кун — истиноди шахсии канал мегирӣ.\n"
            "2️⃣ Онро ба дӯстон фирист. Ҳар касе, ки аз рӯи он ворид шавад, ҳисоб мешавад.\n"
            "3️⃣ Барои ҳар {need} нафар — 1 аккаунт. Он худкор ба ин ҷо меояд.\n"
            "4️⃣ Ҳар рӯз №1 аз рӯи даъватҳо +1 аккаунт мегирад.\n\n"
            "ℹ️ Агар даъватшуда аз канал барояд, дигар ҳисоб намешавад.\n"
            "📦 Ҳамаи аккаунтҳои гирифташуда ҳамеша дар бахши «Аккаунтҳои ман» мемонанд."),
        "share_text": ("🎁 Дар канали CPM_SSM аккаунтҳои пурраро ройгон тақсим мекунанд!\n"
                       "Аз рӯи истиноди ман ворид шав ва аккаунти худро бигир 👇"),
        "menu_title": ("🏠 Менюи асосӣ\n\n"
                       "👥 Даъват шуд: {c}   📦 Аккаунт гирифта шуд: {g}\n\n"
                       "Амалро интихоб кун 👇"),
        "btn_claim_n": "🎁 Гирифтани тӯҳфа ({n})",
        "btn_claim": "🎁 Гирифтани тӯҳфа",
        "btn_link": "🔗 Истиноди ман",
        "btn_getlink": "🔗 Гирифтани истинод",
        "btn_progress": "📊 Пешрафт",
        "btn_top": "🏆 Топ",
        "btn_today": "📅 Топи рӯз",
        "btn_accounts": "📦 Аккаунтҳои ман",
        "btn_help": "❓ Чӣ тавр кор мекунад",
        "btn_channel": "📢 Ба канал гузаштан",
        "btn_review": "📸 Шарҳ гузоштан",
        "btn_lang": "🌐 Забон",
        "btn_back": "⬅️ Меню",
        "btn_home": "🏠 Меню",
        "btn_sub": "📢 Ба канал обуна шудан",
        "btn_subbed": "✅ Ман обуна шудам",
        "btn_share": "📤 Фиристодани истинод",
        "btn_ready": "📨 Паёми тайёр",
        "btn_send_friends": "📤 Ба дӯстон фиристодан",
        "btn_retry": "🔄 Такрор кардан",
        "btn_skip": "Гузаштан",
        "btn_prev": "‹ Қафо",
        "btn_next": "Пеш ›",
        "st_left": "То аккаунти навбатӣ боз {n} нафарро даъват кардан лозим аст",
        "st_total": "👥 Ҳамагӣ даъват шуд: {n}",
        "st_earned": "🏅 Аккаунт ба даст омад: {n}",
        "st_got": "📦 Аллакай гирифта шуд: {n}",
        "st_avail": "🎁 Барои гирифтан дастрас: {n}",
        "progress_title": "📊 Пешрафти шумо:",
        "anon": "Иштирокчӣ",
        "unit": "нафар",
        "you": "← шумо",
        "top_title": "🏆 Топ-10 аз рӯи даъватҳо",
        "top_empty": "🏆 Топ ҳоло холӣ аст. Аввалин шавед — дӯстонро даъват кунед!",
        "top_place": "Ҷои шумо: {p} ({n} нафар)",
        "top_none": "Шумо ҳоло касеро даъват накардаед.",
        "today_title": "📅 Топи рӯз",
        "today_left": "⏳ То охири рӯз: {h} соат {m} дақиқа",
        "today_prize": "🎁 Ғолиб +1 аккаунт мегирад (ҳадди аққал {n} даъватшуда)",
        "today_empty": "Имрӯз ҳоло ҳеҷ кас нест. Ту аввалин шуда метавонӣ! 🚀",
        "today_place": "Ҷои шумо имрӯз: {p} ({n} нафар)",
        "today_none": "Имрӯз шумо ҳоло касеро даъват накардаед.",
        "archive_empty": "📦 Шумо ҳоло аккаунти гирифташуда надоред.",
        "archive_title": "📦 Аккаунтҳои шумо ({t}) саҳ. {p}/{n}",
        "sub_prompt": "Аввал ба канали мо обуна шавед, баъд «Ман обуна шудам»-ро пахш кунед 👇",
        "link_fail": "😔 Истинодро сохта натавонистем. Каме баъдтар кӯшиш кунед.",
        "link_text": ("🔗 Истиноди шахсии шумо:\n{link}\n\n"
                      "Барои ҳар {need} даъватшуда — 1 аккаунт.\n\n{status}"),
        "give_updated": "Баъзе даъватшудагон аз канал баромаданд, ҳисоб навсозӣ шуд.\n\n",
        "give_empty": ("Ҳоло аккаунтҳо тамом шуданд, ба зудӣ илова мекунем ⏳\n"
                       "Баъдтар боз «Гирифтани тӯҳфа»-ро пахш кунед."),
        "gift": ("🎁 Тӯҳфаи шумо:\n\n{data}\n\nТашаккур, ки бо мо ҳастед! ❤️\n"
                 "📦 Ҳамаи аккаунтҳо ҳамеша дар бахши «Аккаунтҳои ман» ҳастанд."),
        "giveaway_win": ("🎉 Табрик, шумо ғолиби розыгрыш шудед!\n\n"
                         "🎁 Ҷоизаи шумо:\n\n{data}\n\nТашаккур, ки бо мо ҳастед! ❤️"),
        "review_ask": ("📸 Лутфан, шарҳ гузоред!\n\n"
                       "Скриншоти аккаунтро ба ин ҷо фиристед — мо онро дар канал нишон медиҳем, "
                       "то дӯстон ҳам хоҳанд тӯҳфа гиранд.\n\n"
                       "⚠️ Логин ва паролро дар скриншот нишон надиҳед."),
        "review_ask_winner": ("🏆 Табрик, ту ғолиб шудӣ!\n\n"
                              "Лутфан, скриншоти аккаунтро фирист — мо онро дар канал "
                              "ҳамчун шарҳи ғолиб нишон медиҳем 🎉\n\n"
                              "⚠️ Логин ва паролро дар скриншот нишон надеҳ."),
        "review_thanks": "Ташаккур барои шарҳ! ❤️ Он баъди санҷиш дар канал пайдо мешавад.",
        "review_published": "🎉 Шарҳи шумо дар канал нашр шуд. Ташаккур!",
        "review_hint": "Мехоҳед шарҳ гузоред? Тугмаро пахш кунед, баъд скриншот фиристед 👇",
        "review_after_only": "Шарҳ гузоштан баъди гирифтани аккаунт имконпазир аст 🎁",
        "new_member": "✅ Узви нав аз рӯи истиноди шумо ворид шуд!\n\n{status}",
        "congrats": "🎉 Табрик! Шумо {c} нафарро даъват кардед!",
        "claim_need": "Ҳоло {c}/{need} даъват шудааст. Боз {r} нафар лозим аст.",
        "claim_all": ("Ҳамаи аккаунтҳои дастрас гирифта шуданд. "
                      "Барои навбатӣ боз {r} нафарро даъват кунед."),
        "daily_win": ("🏆 Шумо — №1 аз рӯи даъватҳо дирӯз ({c} нафар)!\n\n"
                      "🎁 Тӯҳфаи рӯзи шумо:\n\n{data}\n\nТашаккур, ки бо мо ҳастед! ❤️"),
        "lang_prompt": "🌐 Выберите язык / Забонро интихоб кунед / Тилди тандаңыз",
        "invited": ("🎉 Шуморо {who} даъват кард!\n\n"
                    "Дар канали мо аккаунтҳои пурраро ройгон тақсим мекунанд 🎁\n"
                    "Шумо ҳам мехоҳед тӯҳфа гиред? Тугмаро пахш кунед ва истиноди худро гиред 👇"),
    },
}

S["ky"] = {
    "welcome": (
        "👋 Салам!\n\n"
        "Белек — толук аккаунт — алгың келеби? 🎁\n\n"
        "Достторуңду жеке шилтемең аркылуу биздин каналга чакыр:\n"
        "• {n1} адам — 1 аккаунт\n"
        "• {n2} адам — 2 аккаунт\n"
        "• {n3} адам — 3 аккаунт\n"
        "жана ушундай улантылат!\n\n"
        "🏆 Күн сайын чакыруулар боюнча №1 болгон адам +1 аккаунт белек алат!\n\n"
        "Шарт аткарылары менен аккаунт автоматтык түрдө келет.\n\n"
        "Төмөнкү аракетти танда 👇"),
    "help": (
        "❓ Бул кантип иштейт\n\n"
        "1️⃣ «Менин шилтемем» баскычын бас — каналга жеке шилтеме аласың.\n"
        "2️⃣ Аны досторуңа жөнөт. Ал аркылуу кошулган ар бир адам эсептелет.\n"
        "3️⃣ Ар {need} адам үчүн — 1 аккаунт. Ал ушул жерге автоматтык түрдө келет.\n"
        "4️⃣ Күн сайын чакыруулар боюнча №1 болгон адам +1 аккаунт алат.\n\n"
        "ℹ️ Чакырылган адам каналдан чыгып кетсе, ал эсептен чыгат.\n"
        "📦 Алынган бардык аккаунттар ар дайым «Менин аккаунттарым» бөлүмүндө сакталат."),
    "share_text": ("🎁 CPM_SSM каналында толук аккаунттар акысыз таратылат!\n"
                   "Менин шилтемем аркылуу кирип, өзүңдүкүн ал 👇"),
    "menu_title": ("🏠 Башкы меню\n\n"
                   "👥 Чакырылды: {c}   📦 Алынган аккаунт: {g}\n\n"
                   "Аракетти танда 👇"),
    "btn_claim_n": "🎁 Белек алуу ({n})",
    "btn_claim": "🎁 Белек алуу",
    "btn_link": "🔗 Менин шилтемем",
    "btn_getlink": "🔗 Шилтеме алуу",
    "btn_progress": "📊 Прогресс",
    "btn_top": "🏆 Топ",
    "btn_today": "📅 Күндүн топу",
    "btn_accounts": "📦 Менин аккаунттарым",
    "btn_help": "❓ Бул кантип иштейт",
    "btn_channel": "📢 Каналга өтүү",
    "btn_review": "📸 Пикир калтыруу",
    "btn_lang": "🌐 Тил",
    "btn_back": "⬅️ Меню",
    "btn_home": "🏠 Меню",
    "btn_sub": "📢 Каналга жазылуу",
    "btn_subbed": "✅ Мен жазылдым",
    "btn_share": "📤 Шилтемени бөлүшүү",
    "btn_ready": "📨 Даяр билдирүү",
    "btn_send_friends": "📤 Достторго жөнөтүү",
    "btn_retry": "🔄 Кайталоо",
    "btn_skip": "Өткөрүп жиберүү",
    "btn_prev": "‹ Артка",
    "btn_next": "Алдыга ›",
    "st_left": "Кийинки аккаунтка чейин чакырыш керек: {n}",
    "st_total": "👥 Жалпы чакырылды: {n}",
    "st_earned": "🏅 Тапкан аккаунттар: {n}",
    "st_got": "📦 Мурунтан алынды: {n}",
    "st_avail": "🎁 Алууга жеткиликтүү: {n}",
    "progress_title": "📊 Сенин прогрессиң:",
    "anon": "Катышуучу",
    "unit": "адам",
    "you": "← сен",
    "top_title": "🏆 Чакыруулар боюнча Топ-10",
    "top_empty": "🏆 Топ азырынча бош. Биринчи бол — достторуңду чакыр!",
    "top_place": "Сенин орунуң: {p} ({n} адам)",
    "top_none": "Сен азырынча эч кимди чакыра элексиң.",
    "today_title": "📅 Күндүн топу",
    "today_left": "⏳ Күндүн аягына чейин: {h} саат {m} мүнөт",
    "today_prize": "🎁 Жеңүүчү +1 аккаунт алат (кеминде {n} чакырылган)",
    "today_empty": "Бүгүн азырынча эч ким жок. Биринчи боло аласың! 🚀",
    "today_place": "Бүгүнкү орунуң: {p} ({n} адам)",
    "today_none": "Бүгүн сен азырынча эч кимди чакыра элексиң.",
    "archive_empty": "📦 Сенде азырынча алынган аккаунт жок.",
    "archive_title": "📦 Сенин аккаунттарың ({t}) бет {p}/{n}",
    "sub_prompt": "Адегенде биздин каналга жазыл, анан «Мен жазылдым» баскычын бас 👇",
    "link_fail": "😔 Шилтемени түзө алган жокпуз. Бираздан кийин кайра аракет кыл.",
    "link_text": ("🔗 Сенин жеке шилтемең:\n{link}\n\n"
                  "Ар {need} чакырылган адам үчүн — 1 аккаунт.\n\n{status}"),
    "give_updated": "Кээ бир чакырылгандар каналдан чыгып кетти, эсеп жаңыртылды.\n\n",
    "give_empty": ("Азыр аккаунттар түгөндү, жакында кошобуз ⏳\n"
                   "Кийинчерээк «Белек алуу» баскычын кайра бас."),
    "gift": ("🎁 Сенин белегиң:\n\n{data}\n\nБизде болгонуң үчүн рахмат! ❤️\n"
             "📦 Бардык аккаунттар ар дайым «Менин аккаунттарым» бөлүмүндө бар."),
    "giveaway_win": ("🎉 Куттуктайбыз, сен розыгрыштын жеңүүчүсүсүң!\n\n"
                     "🎁 Сенин байгең:\n\n{data}\n\nБизде болгонуң үчүн рахмат! ❤️"),
    "review_ask": ("📸 Сураныч, пикир калтыр!\n\n"
                   "Аккаунттан скриншотту ушул жакка жөнөт — биз аны каналда көрсөтөбүз, "
                   "достор да белек алгысы келсин.\n\n"
                   "⚠️ Скриншотто логин менен сырсөздү көрсөтпө."),
    "review_ask_winner": ("🏆 Куттуктайбыз, сен жеңүүчүсүң!\n\n"
                          "Сураныч, аккаунттан скриншот жөнөт — биз аны каналда "
                          "жеңүүчүнүн пикири катары көрсөтөбүз 🎉\n\n"
                          "⚠️ Скриншотто логин менен сырсөздү көрсөтпө."),
    "review_thanks": "Пикир үчүн рахмат! ❤️ Ал текшерүүдөн кийин каналда пайда болот.",
    "review_published": "🎉 Сенин пикириң каналда жарыяланды. Рахмат!",
    "review_hint": "Пикир калтыргың келеби? Баскычты бас, анан скриншот жөнөт 👇",
    "review_after_only": "Пикирди аккаунт алгандан кийин калтырууга болот 🎁",
    "new_member": "✅ Сенин шилтемең аркылуу жаңы мүчө кошулду!\n\n{status}",
    "congrats": "🎉 Куттуктайбыз! Сен {c} адамды чакырдың!",
    "claim_need": "Азырынча {c}/{need} чакырылды. Дагы {r} адам керек.",
    "claim_all": ("Жеткиликтүү бардык аккаунттар алынды. "
                  "Кийинкиси үчүн дагы {r} адамды чакыр."),
    "daily_win": ("🏆 Сен кечээ чакыруулар боюнча №1 болдуң ({c} адам)!\n\n"
                  "🎁 Сенин күндүн белегиң:\n\n{data}\n\nБизде болгонуң үчүн рахмат! ❤️"),
    "lang_prompt": "🌐 Выберите язык / Забонро интихоб кунед / Тилди тандаңыз",
    "invited": ("🎉 Сени {who} чакырды!\n\n"
                "Биздин каналда толук аккаунттар акысыз таратылат 🎁\n"
                "Сен да белек алгың келеби? Төмөнкү баскычты бас да, өз шилтемеңди ал 👇"),
}

S["ru"]["promo_after"] = "📢 Больше подарков и предложений — в наших каналах 👇"
S["tg"]["promo_after"] = "📢 Тӯҳфа ва пешниҳодҳои бештар — дар каналҳои мо 👇"
S["ky"]["promo_after"] = "📢 Көбүрөөк белектер жана сунуштар — биздин каналдарда 👇"

S["ru"].update({
    "camp_text": ("🎯 Задание: {title}\n\n"
                  "Пригласи {need} человек в канал по своей ссылке — получишь 1 аккаунт 🎁\n\n"
                  "🔗 Твоя ссылка:\n{link}\n\n{bar} {n}/{need}\n"
                  "👥 Приглашено: {total}\n🎁 Получено аккаунтов: {got}\n🎁 Доступно: {avail}"),
    "camp_share": "🎁 Заходи в канал «{title}» по моей ссылке 👇",
    "camp_new_member": "✅ Новый участник вступил в «{title}» по твоей ссылке!\n\n{bar} {n}/{need}",
    "camp_win": ("🎉 Задание «{title}» выполнено — приглашено {c} человек!\n\n"
                 "🎁 Твой подарок:\n\n{data}\n\nСпасибо, что с нами! ❤️"),
    "camp_closed": "Это задание завершено или выключено 🙁",
    "btn_open_ch": "📢 Открыть канал",
})
S["tg"].update({
    "camp_text": ("🎯 Вазифа: {title}\n\n"
                  "{need} нафарро бо истиноди худ ба канал даъват кун — 1 аккаунт мегирӣ 🎁\n\n"
                  "🔗 Истиноди ту:\n{link}\n\n{bar} {n}/{need}\n"
                  "👥 Даъват шуд: {total}\n🎁 Аккаунт гирифта шуд: {got}\n🎁 Дастрас: {avail}"),
    "camp_share": "🎁 Ба канали «{title}» аз рӯи истиноди ман ворид шав 👇",
    "camp_new_member": "✅ Узви нав ба «{title}» аз рӯи истиноди ту ворид шуд!\n\n{bar} {n}/{need}",
    "camp_win": ("🎉 Вазифаи «{title}» иҷро шуд — {c} нафар даъват шуд!\n\n"
                 "🎁 Тӯҳфаи ту:\n\n{data}\n\nТашаккур, ки бо мо ҳастӣ! ❤️"),
    "camp_closed": "Ин вазифа тамом шудааст ё хомӯш аст 🙁",
    "btn_open_ch": "📢 Кушодани канал",
})
S["ky"].update({
    "camp_text": ("🎯 Тапшырма: {title}\n\n"
                  "Өз шилтемең аркылуу каналга {need} адам чакыр — 1 аккаунт аласың 🎁\n\n"
                  "🔗 Сенин шилтемең:\n{link}\n\n{bar} {n}/{need}\n"
                  "👥 Чакырылды: {total}\n🎁 Алынган аккаунт: {got}\n🎁 Жеткиликтүү: {avail}"),
    "camp_share": "🎁 «{title}» каналына менин шилтемем аркылуу кир 👇",
    "camp_new_member": "✅ «{title}» каналына сенин шилтемең аркылуу жаңы мүчө кошулду!\n\n{bar} {n}/{need}",
    "camp_win": ("🎉 «{title}» тапшырмасы аткарылды — {c} адам чакырылды!\n\n"
                 "🎁 Сенин белегиң:\n\n{data}\n\nБизде болгонуң үчүн рахмат! ❤️"),
    "camp_closed": "Бул тапшырма аяктады же өчүрүлдү 🙁",
    "btn_open_ch": "📢 Каналды ачуу",
})

PW_LABEL = {"ru": "Пароль", "tg": "Парол", "ky": "Сырсөз"}


def pw_label(uid):
    return PW_LABEL.get(lang_of(uid), "Пароль")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DB_PATH") or os.path.join(BASE_DIR, "ref.db")
EMOJI_BACKUP = os.path.join(BASE_DIR, "emoji_backup.json")
# Агар хоҳед, эмодзиҳои премиумро ин ҷо ҳамеша сабт кунед: {"🎁": "ID", "📦": "ID"}
EMOJI_DEFAULTS = {}

db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("CREATE TABLE IF NOT EXISTS links(user_id INTEGER PRIMARY KEY, link TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS joins(owner_id INTEGER, member_id INTEGER, PRIMARY KEY(owner_id, member_id))")
try:
    db.execute("ALTER TABLE joins ADD COLUMN ts INTEGER")
except sqlite3.OperationalError:
    pass
db.execute("CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS claims(user_id INTEGER PRIMARY KEY)")
db.execute("CREATE TABLE IF NOT EXISTS rewards(user_id INTEGER PRIMARY KEY, claimed INTEGER)")
db.execute("CREATE TABLE IF NOT EXISTS notif(msg_id INTEGER PRIMARY KEY, user_id INTEGER)")
db.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY)")
db.execute("CREATE TABLE IF NOT EXISTS profiles(user_id INTEGER PRIMARY KEY, name TEXT, username TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS stock(id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, used_by INTEGER)")
try:
    db.execute("ALTER TABLE stock ADD COLUMN used_at INTEGER")
except sqlite3.OperationalError:
    pass
db.execute("CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, file_id TEXT, ts INTEGER, status TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS review_wait(user_id INTEGER PRIMARY KEY)")
for _tbl, _col in (("reviews", "kind"), ("reviews", "note"), ("review_wait", "kind"), ("review_wait", "note")):
    try:
        db.execute(f"ALTER TABLE {_tbl} ADD COLUMN {_col} TEXT")
    except sqlite3.OperationalError:
        pass
db.execute("CREATE TABLE IF NOT EXISTS lang(user_id INTEGER PRIMARY KEY, lang TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS emoji_map(emoji TEXT PRIMARY KEY, cid TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS invited_msg(user_id INTEGER PRIMARY KEY)")
db.execute("CREATE TABLE IF NOT EXISTS prize_log(msg_id INTEGER PRIMARY KEY)")
db.execute("CREATE TABLE IF NOT EXISTS pending_prize(user_id INTEGER PRIMARY KEY)")
db.execute("CREATE TABLE IF NOT EXISTS promo_channels(id INTEGER PRIMARY KEY AUTOINCREMENT, "
           "title TEXT, url TEXT, active INTEGER DEFAULT 1, icon TEXT, fb TEXT)")
for _col, _typ in (("chat_id", "INTEGER"), ("need", "INTEGER DEFAULT 0")):
    try:
        db.execute(f"ALTER TABLE promo_channels ADD COLUMN {_col} {_typ}")
    except sqlite3.OperationalError:
        pass
db.execute("CREATE TABLE IF NOT EXISTS c_links(camp_id INTEGER, user_id INTEGER, link TEXT, "
           "PRIMARY KEY(camp_id, user_id))")
db.execute("CREATE TABLE IF NOT EXISTS c_joins(camp_id INTEGER, owner_id INTEGER, member_id INTEGER, ts INTEGER, "
           "PRIMARY KEY(camp_id, member_id))")
db.execute("CREATE TABLE IF NOT EXISTS c_rewards(camp_id INTEGER, user_id INTEGER, claimed INTEGER, "
           "PRIMARY KEY(camp_id, user_id))")
db.execute("INSERT OR IGNORE INTO rewards SELECT user_id, 1 FROM claims")
db.commit()


def get_setting(key, default=None):
    r = db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return r[0] if r else default


def set_setting(key, value):
    db.execute("INSERT OR REPLACE INTO settings VALUES(?,?)", (key, str(value)))
    db.commit()


# ======================= Telegram API =======================

def api(method, **params):
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/{method}",
        data=json.dumps(params).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)["result"]
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode("utf-8", "ignore"))


EMOJI_MAP = {}   # эмодзи -> custom_emoji_id (премиум)
FALLBACK = {}    # (матни тугма, id) -> эмодзии оддӣ (барои бозгашт)


def norm_emoji(e):
    return e.replace("\ufe0f", "")


def save_emoji_backup():
    try:
        with open(EMOJI_BACKUP, "w", encoding="utf-8") as f:
            json.dump(EMOJI_MAP, f, ensure_ascii=False, indent=1)
    except Exception as e:
        print("emoji backup error:", e)


def load_emoji():
    """Эмодзиҳо аз 3 ҷой: база, emoji_backup.json, EMOJI_DEFAULTS. Гум намешаванд."""
    EMOJI_MAP.clear()
    for e, c in db.execute("SELECT emoji, cid FROM emoji_map").fetchall():
        EMOJI_MAP[e] = c
    try:
        with open(EMOJI_BACKUP, encoding="utf-8") as f:
            backup = json.load(f)
    except Exception:
        backup = {}
    for src in (backup, EMOJI_DEFAULTS):
        for e, c in src.items():
            e = norm_emoji(e)
            if e not in EMOJI_MAP:
                EMOJI_MAP[e] = c
                db.execute("INSERT OR IGNORE INTO emoji_map VALUES(?,?)", (e, c))
    db.commit()
    save_emoji_backup()


_last_backup = [0]


def backup_db(force=False):
    """Ҳар 6 соат нусхаи базаро дар ref.db.bak нигоҳ медорад."""
    if not force and time.time() - _last_backup[0] < 6 * 3600:
        return
    _last_backup[0] = time.time()
    try:
        dst = sqlite3.connect(DB_PATH + ".bak")
        db.backup(dst)
        dst.close()
    except Exception as e:
        print("db backup error:", e)


def _btn(text, extra, style=None):
    prefix, _, rest = text.partition(" ")
    cid = EMOJI_MAP.get(norm_emoji(prefix)) if rest else None
    if cid:
        FALLBACK[(rest, cid)] = prefix
        b = {"text": rest, "icon_custom_emoji_id": cid}
    else:
        b = {"text": text}
    if style and BUTTON_STYLES:
        b["style"] = style
    b.update(extra)
    return b


def cb(text, data, style=None):
    return _btn(text, {"callback_data": data}, style)


def url_btn(text, url, style=None):
    return _btn(text, {"url": url}, style)


def is_fancy(buttons):
    return bool(buttons) and any("icon_custom_emoji_id" in b or "style" in b
                                 for row in buttons["inline_keyboard"] for b in row)


def strip_fancy(buttons):
    """Премиум-эмодзи ва рангҳоро мебарорад, эмодзии оддиро ба матн бармегардонад."""
    rows = []
    for row in buttons["inline_keyboard"]:
        new_row = []
        for b in row:
            b = dict(b)
            cid = b.pop("icon_custom_emoji_id", None)
            b.pop("style", None)
            if cid:
                pre = FALLBACK.get((b["text"], cid), "")
                b["text"] = (pre + " " + b["text"]).strip()
            new_row.append(b)
        rows.append(new_row)
    return {"inline_keyboard": rows}


def markup(*rows):
    return {"inline_keyboard": [list(r) for r in rows]}


def _emoji_re():
    keys = sorted(EMOJI_MAP, key=len, reverse=True)
    if not keys:
        return None
    return re.compile("|".join("\ufe0f?".join(re.escape(ch) for ch in k) + "\ufe0f?" for k in keys))


def premium_text(text, parse_mode):
    """Эмодзиҳои оддиро дар матн ба премиум иваз мекунад. -> (text, extra_params)."""
    pat = _emoji_re()
    if not pat or not text:
        return text, {}
    if parse_mode == "HTML":
        return pat.sub(lambda m: '<tg-emoji emoji-id="%s">%s</tg-emoji>'
                       % (EMOJI_MAP[norm_emoji(m.group(0))], m.group(0)), text), {}
    if parse_mode is None:
        ents, pos, last = [], 0, 0
        for m in pat.finditer(text):
            pos += len(text[last:m.start()].encode("utf-16-le")) // 2
            ln = len(m.group(0).encode("utf-16-le")) // 2
            ents.append({"type": "custom_emoji", "offset": pos, "length": ln,
                         "custom_emoji_id": EMOJI_MAP[norm_emoji(m.group(0))]})
            pos += ln
            last = m.end()
        if ents:
            return text, {"entities": ents}
    return text, {}


def strip_copy(buttons):
    """Тугмаҳои copy_text-ро мебарорад (агар Telegram қабул накунад)."""
    rows = [[b for b in row if "copy_text" not in b] for row in buttons["inline_keyboard"]]
    return {"inline_keyboard": [r for r in rows if r]}


def has_copy(buttons):
    return bool(buttons) and any("copy_text" in b for row in buttons["inline_keyboard"] for b in row)


def plain_buttons(buttons):
    """Тугмаҳо бе премиум, ранг ва нусхабардорӣ (охирин чораи эҳтиётӣ)."""
    return strip_copy(strip_fancy(buttons)) if buttons else buttons


def copy_btn(text, value):
    """Тугмаи нусхабардорӣ; эмодзии аввал метавонад премиум шавад."""
    return _btn(text, {"copy_text": {"text": value[:256]}})


def _attempts(text, buttons, parse_mode):
    """Тартиби кӯшишҳо: пурра -> бе премиум дар матн -> бе премиум/ранг/нусхабардорӣ."""
    out = [(buttons, True)]
    t2, extra = premium_text(text, parse_mode)
    if extra or t2 != text:
        out.append((buttons, False))
    if is_fancy(buttons) or has_copy(buttons):
        out.append((plain_buttons(buttons), False))
    return out


def _send(chat_id, text, buttons, parse_mode=None, premium=True):
    extra = {}
    if premium:
        text, extra = premium_text(text, parse_mode)
    params = {"chat_id": chat_id, "text": text, **extra}
    if parse_mode:
        params["parse_mode"] = parse_mode
    if buttons:
        params["reply_markup"] = buttons
    return api("sendMessage", **params)


def is_forbidden(e):
    t = str(e)
    return "403" in t or "Forbidden" in t or "chat not found" in t


def send(chat_id, text, buttons=None, parse_mode=None):
    for b, prem in _attempts(text, buttons, parse_mode):
        try:
            return _send(chat_id, text, b, parse_mode, prem)
        except Exception as e:
            if is_forbidden(e):
                print(f"send skipped: {chat_id} недоступен (бот заблокирован или /start не нажат)")
                return None
            print("send failed, trying fallback:", e)
    return None


def edit(chat_id, msg_id, text, buttons=None, parse_mode=None):
    """Паёми мавҷударо иваз мекунад (чат тоза мемонад). Агар нашавад — паёми нав."""
    if not msg_id:
        return send(chat_id, text, buttons, parse_mode)

    def _edit(b, prem):
        t, extra = premium_text(text, parse_mode) if prem else (text, {})
        params = {"chat_id": chat_id, "message_id": msg_id, "text": t, **extra}
        if parse_mode:
            params["parse_mode"] = parse_mode
        if b:
            params["reply_markup"] = b
        return api("editMessageText", **params)

    for b, prem in _attempts(text, buttons, parse_mode):
        try:
            return _edit(b, prem)
        except Exception as e:
            if "not modified" in str(e):
                return None
            if is_forbidden(e):
                return None
    return send(chat_id, text, buttons, parse_mode)


def show(chat_id, msg_id, screen):
    text, kb = screen[0], screen[1]
    mode = screen[2] if len(screen) > 2 else None
    return edit(chat_id, msg_id, text, kb, mode)


# ======================= Забон (i18n) =======================

def lang_of(uid):
    if uid is None:
        return DEFAULT_LANG
    r = db.execute("SELECT lang FROM lang WHERE user_id=?", (uid,)).fetchone()
    return r[0] if r and r[0] in S else DEFAULT_LANG


def has_lang(uid):
    return db.execute("SELECT 1 FROM lang WHERE user_id=?", (uid,)).fetchone() is not None


def set_lang(uid, code):
    db.execute("INSERT OR REPLACE INTO lang VALUES(?,?)", (uid, code))
    db.commit()


def tr(uid, key, **kw):
    lang = lang_of(uid)
    text = S[lang].get(key) or S[DEFAULT_LANG][key]
    return text.format(**kw) if kw else text


def lang_kb(mode, uid=None):
    rows = [[cb("🇷🇺 Русский", f"lang:ru:{mode}"), cb("🇹🇯 Тоҷикӣ", f"lang:tg:{mode}")],
            [cb("🇰🇬 Кыргызча", f"lang:ky:{mode}")]]
    if mode == "m":
        rows.append(back(uid))
    return markup(*rows)


# ======================= Ҳисобҳо =======================

def count(uid):
    return db.execute("SELECT COUNT(*) FROM joins WHERE owner_id=?", (uid,)).fetchone()[0]


def claimed(uid):
    row = db.execute("SELECT claimed FROM rewards WHERE user_id=?", (uid,)).fetchone()
    return row[0] if row else 0


def available(uid):
    return max(0, count(uid) // NEED - claimed(uid))


def stock_left():
    return db.execute("SELECT COUNT(*) FROM stock WHERE used_by IS NULL").fetchone()[0]


def status(uid):
    cnt = count(uid)
    n = cnt % NEED
    return (f"{'▓' * n + '░' * (NEED - n)} {n}/{NEED}\n"
            + tr(uid, "st_left", n=NEED - n) + "\n\n"
            + tr(uid, "st_total", n=cnt) + "\n"
            + tr(uid, "st_earned", n=cnt // NEED) + "\n"
            + tr(uid, "st_got", n=claimed(uid)) + "\n"
            + tr(uid, "st_avail", n=available(uid)))


def day_key(ts=None):
    """Рақами рӯз бо ҳисоби TZ_OFFSET."""
    return int(((ts if ts is not None else time.time()) + TZ_OFFSET) // 86400)


def day_range(key):
    start = key * 86400 - TZ_OFFSET
    return start, start + 86400


def day_count(uid, start, end):
    return db.execute("SELECT COUNT(*) FROM joins WHERE owner_id=? AND ts>=? AND ts<?",
                      (uid, start, end)).fetchone()[0]


def check_member(uid, chat=None):
    """True/False — обуна ҳаст ё не. None — санҷиш ба хато дучор шуд."""
    try:
        r = api("getChatMember", chat_id=chat or CHANNEL_ID, user_id=uid)
        st = r["status"]
        return (st in ("member", "administrator", "creator")
                or (st == "restricted" and r.get("is_member", False)))
    except Exception as e:
        print("check_member error:", e)
        return None


def get_link(user):
    uid = user["id"]
    row = db.execute("SELECT link FROM links WHERE user_id=?", (uid,)).fetchone()
    if row:
        return row[0]
    name = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or str(uid)
    inv = api("createChatInviteLink", chat_id=CHANNEL_ID, name=name[:32])
    link = inv["invite_link"]
    db.execute("INSERT INTO links VALUES(?,?)", (uid, link))
    db.commit()
    return link


def remember(user):
    name = (user.get("first_name", "") + " " + user.get("last_name", "")).strip()
    db.execute("INSERT OR REPLACE INTO profiles VALUES(?,?,?)",
               (user["id"], name, user.get("username", "")))
    db.commit()


def verify_members(owner):
    """Касонеро, ки аз канал баромадаанд, аз ҳисоб мебарорад."""
    removed = 0
    for (m,) in db.execute("SELECT member_id FROM joins WHERE owner_id=?", (owner,)).fetchall():
        if check_member(m) is False:
            db.execute("DELETE FROM joins WHERE owner_id=? AND member_id=?", (owner, m))
            removed += 1
    db.commit()
    return removed


def public_name(oid, viewer=None):
    r = db.execute("SELECT name, username FROM profiles WHERE user_id=?", (oid,)).fetchone()
    name, uname = r if r else ("", "")
    return (name or (("@" + uname) if uname else tr(viewer, "anon")))[:20]


def member_name(mid):
    row = db.execute("SELECT name, username FROM profiles WHERE user_id=?", (mid,)).fetchone()
    name, uname = row if row else ("", "")
    if not name and not uname:
        try:
            u = api("getChatMember", chat_id=CHANNEL_ID, user_id=mid)["user"]
            name = (u.get("first_name", "") + " " + u.get("last_name", "")).strip()
            uname = u.get("username", "")
        except Exception:
            pass
    s = name or str(mid)
    if uname:
        s += f" (@{uname})"
    return f"{s} [{mid}]"


# ======================= Корти зебои аккаунт (Email + Парол) =======================

def parse_account(data):
    """Аккаунтро ба (email, парол) ҷудо мекунад.
    Форматҳо: «email:parol», «email parol», ё ду сатр. Агар нашавад — (None, None)."""
    data = (data or "").strip()
    if "\n" in data:
        a, b = data.split("\n", 1)
    elif ":" in data:
        a, b = data.split(":", 1)
    elif " " in data:
        a, b = data.split(None, 1)
    else:
        return None, None
    a, b = a.strip(), b.strip()
    return (a, b) if a and b else (None, None)


def account_card(uid, data, n=None):
    """Корти HTML + рӯйхати тугмаҳои нусхабардорӣ."""
    e, p = parse_account(data)
    head = f"<b>Аккаунт №{n}</b>\n" if n else ""
    if not e:
        return head + f"<code>{html.escape(data)}</code>", []
    pw = pw_label(uid)
    card = (head + "━━━━━━━━━━━━━━\n"
            f"📧 <b>Email</b>\n<code>{html.escape(e)}</code>\n\n"
            f"🔑 <b>{pw}</b>\n<code>{html.escape(p)}</code>\n"
            "━━━━━━━━━━━━━━")
    btns = [copy_btn("📋 Email", e), copy_btn("📋 " + pw, p)]
    return card, btns


def send_gift(uid, key, datas, **fmt):
    """Тӯҳфаро ҳамчун корти зебо мефиристад. Агар тугмаҳои нусхабардорӣ кор накунанд,
    бе онҳо такроран мефиристад (то тӯҳфа ҳатман расад)."""
    cards, btns = [], []
    for i, d in enumerate(datas, 1):
        c, b = account_card(uid, d, i if len(datas) > 1 else None)
        cards.append(c)
        if len(datas) == 1:
            btns = b
    text = tr(uid, key, data="\n\n".join(cards), **fmt)
    tail = [[cb(tr(uid, "btn_accounts"), "myacc")], back(uid)]
    ok = send(uid, text, markup(*(([btns] if btns else []) + tail)), parse_mode="HTML")
    if not ok and btns:
        ok = send(uid, text, markup(*tail), parse_mode="HTML")
    if ok:
        send_promo(uid)
    return ok


# ======================= Экранҳои корбар =======================

def back(uid):
    return [cb(tr(uid, "btn_back"), "menu")]


def claim_kb(uid):
    return markup([cb(tr(uid, "btn_claim"), "claim", "success")], back(uid))


def has_accounts(uid):
    return db.execute("SELECT 1 FROM stock WHERE used_by=? LIMIT 1", (uid,)).fetchone() is not None


def menu_kb(uid=None):
    rows = []
    av = available(uid) if uid else 0
    if av > 0:
        rows.append([cb(tr(uid, "btn_claim_n", n=av), "claim", "success")])
    rows += [
        [cb(tr(uid, "btn_link"), "getlink"), cb(tr(uid, "btn_progress"), "progress")],
        [cb(tr(uid, "btn_top"), "top"), cb(tr(uid, "btn_today"), "today")],
        [cb(tr(uid, "btn_accounts"), "myacc"), cb(tr(uid, "btn_help"), "help")],
        [url_btn(tr(uid, "btn_channel"), CHANNEL_URL), cb(tr(uid, "btn_lang"), "lang")],
    ]
    if uid and has_accounts(uid):
        rows.insert(len(rows) - 1, [cb(tr(uid, "btn_review"), "review")])
    if promo_on("promo_menu"):
        rows += promo_rows()
    if uid == ADMIN_ID:
        rows.append([cb("⚙️ Админ-панель", "admin")])
    return markup(*rows)


def screen_menu(uid, welcome=False):
    if welcome:
        return tr(uid, "welcome", n1=NEED, n2=NEED * 2, n3=NEED * 3), menu_kb(uid)
    return tr(uid, "menu_title", c=count(uid), g=claimed(uid)), menu_kb(uid)


def screen_progress(uid):
    kb_rows = []
    if available(uid) > 0:
        kb_rows.append([cb(tr(uid, "btn_claim"), "claim", "success")])
    kb_rows.append([cb(tr(uid, "btn_link"), "getlink")])
    kb_rows.append(back(uid))
    return tr(uid, "progress_title") + "\n\n" + status(uid), markup(*kb_rows)


def screen_help(uid):
    return tr(uid, "help", need=NEED), markup([cb(tr(uid, "btn_getlink"), "getlink")], back(uid))


def screen_top(uid):
    rows = db.execute(
        "SELECT owner_id, COUNT(*) AS c FROM joins GROUP BY owner_id ORDER BY c DESC LIMIT 10"
    ).fetchall()
    kb = markup([cb(tr(uid, "btn_link"), "getlink"), cb(tr(uid, "btn_progress"), "progress")],
                back(uid))
    if not rows:
        return tr(uid, "top_empty"), kb
    medals = ["🥇", "🥈", "🥉"]
    unit = tr(uid, "unit")
    lines = [tr(uid, "top_title") + "\n"]
    for i, (oid, c) in enumerate(rows):
        mark = medals[i] if i < 3 else f"{i + 1}."
        me = " " + tr(uid, "you") if oid == uid else ""
        lines.append(f"{mark} {public_name(oid, uid)} — {c} {unit}{me}")
    my = count(uid)
    if my > 0 and uid not in [r[0] for r in rows]:
        place = db.execute(
            "SELECT COUNT(*) FROM (SELECT owner_id FROM joins GROUP BY owner_id "
            "HAVING COUNT(*)>?)", (my,)).fetchone()[0] + 1
        lines.append("\n" + tr(uid, "top_place", p=place, n=my))
    elif my == 0:
        lines.append("\n" + tr(uid, "top_none"))
    return "\n".join(lines), kb


def screen_today(uid):
    start, end = day_range(day_key())
    rows = db.execute(
        "SELECT owner_id, COUNT(*) c FROM joins WHERE ts>=? AND ts<? "
        "GROUP BY owner_id ORDER BY c DESC, MAX(ts) ASC LIMIT 10", (start, end)).fetchall()
    left = max(0, int(end - time.time()))
    unit = tr(uid, "unit")
    lines = [tr(uid, "today_title") + "\n",
             tr(uid, "today_left", h=left // 3600, m=left % 3600 // 60),
             tr(uid, "today_prize", n=DAILY_MIN) + "\n"]
    if not rows:
        lines.append(tr(uid, "today_empty"))
    else:
        medals = ["🥇", "🥈", "🥉"]
        for i, (oid, c) in enumerate(rows):
            mark = medals[i] if i < 3 else f"{i + 1}."
            me = " " + tr(uid, "you") if oid == uid else ""
            lines.append(f"{mark} {public_name(oid, uid)} — {c} {unit}{me}")
    mine = day_count(uid, start, end)
    if mine > 0 and uid not in [r[0] for r in rows]:
        place = db.execute(
            "SELECT COUNT(*) FROM (SELECT owner_id FROM joins WHERE ts>=? AND ts<? "
            "GROUP BY owner_id HAVING COUNT(*)>?)", (start, end, mine)).fetchone()[0] + 1
        lines.append("\n" + tr(uid, "today_place", p=place, n=mine))
    elif mine == 0:
        lines.append("\n" + tr(uid, "today_none"))
    return "\n".join(lines), markup([cb(tr(uid, "btn_link"), "getlink")], back(uid))


def screen_archive(uid, page=0):
    total = db.execute("SELECT COUNT(*) FROM stock WHERE used_by=?", (uid,)).fetchone()[0]
    if total == 0:
        return (tr(uid, "archive_empty") + "\n\n" + status(uid),
                markup([cb(tr(uid, "btn_link"), "getlink")], back(uid)))
    pages = (total + PAGE - 1) // PAGE
    page = max(0, min(page, pages - 1))
    rows = db.execute(
        "SELECT data, used_at FROM stock WHERE used_by=? "
        "ORDER BY COALESCE(used_at,0) DESC, id DESC LIMIT ? OFFSET ?",
        (uid, PAGE, page * PAGE)).fetchall()
    pw = pw_label(uid)
    parts = [f"<b>{html.escape(tr(uid, 'archive_title', t=total, p=page + 1, n=pages))}</b>"]
    kb_rows = []
    for i, (data, ts) in enumerate(rows, page * PAGE + 1):
        when = time.strftime("%d.%m.%Y %H:%M", time.gmtime(ts + TZ_OFFSET)) if ts else "—"
        e, p = parse_account(data)
        if e:
            parts.append(f"━━━━━━━━━━━━━━\n<b>№{i}</b>  🕒 {when}\n"
                         f"📧 <code>{html.escape(e)}</code>\n"
                         f"🔑 <code>{html.escape(p)}</code>")
            kb_rows.append([copy_btn(f"📋 №{i} Email", e), copy_btn(f"📋 №{i} {pw}", p)])
        else:
            parts.append(f"━━━━━━━━━━━━━━\n<b>№{i}</b>  🕒 {when}\n<code>{html.escape(data)}</code>")
    parts.append("━━━━━━━━━━━━━━")
    nav = []
    if page > 0:
        nav.append(cb(tr(uid, "btn_prev"), f"acc:{page - 1}"))
    if page < pages - 1:
        nav.append(cb(tr(uid, "btn_next"), f"acc:{page + 1}"))
    if nav:
        kb_rows.append(nav)
    kb_rows.append(back(uid))
    return "\n\n".join(parts), markup(*kb_rows), "HTML"


def sub_prompt(uid, retry):
    return (tr(uid, "sub_prompt"),
            markup([url_btn(tr(uid, "btn_sub"), CHANNEL_URL)],
                   [cb(tr(uid, "btn_subbed"), retry)], back(uid)))


def share_url(link, uid):
    return ("https://t.me/share/url?url=" + urllib.parse.quote(link)
            + "&text=" + urllib.parse.quote(tr(uid, "share_text")))


def screen_link(user):
    uid = user["id"]
    if check_member(uid) is False:
        return sub_prompt(uid, "getlink")
    try:
        link = get_link(user)
    except Exception as e:
        print("get_link error:", e)
        return (tr(uid, "link_fail"),
                markup([cb(tr(uid, "btn_retry"), "getlink")], back(uid)))
    rows = [[url_btn(tr(uid, "btn_share"), share_url(link, uid))],
            [cb(tr(uid, "btn_ready"), "promo"), cb(tr(uid, "btn_progress"), "progress")]]
    if available(uid) > 0:
        rows.insert(0, [cb(tr(uid, "btn_claim"), "claim", "success")])
    rows.append(back(uid))
    return tr(uid, "link_text", link=link, need=NEED, status=status(uid)), markup(*rows)


def screen_promo(user):
    uid = user["id"]
    try:
        link = get_link(user)
    except Exception as e:
        print("get_link error:", e)
        return (tr(uid, "link_fail"),
                markup([cb(tr(uid, "btn_retry"), "promo")], back(uid)))
    return (tr(uid, "share_text") + "\n" + link,
            markup([url_btn(tr(uid, "btn_send_friends"), share_url(link, uid))],
                   [cb(tr(uid, "btn_link"), "getlink")], back(uid)))


# ======================= Паём ба даъватшуда =======================

def notify_invited(member):
    """Ба даъватшуда паёми шахсӣ мефиристад (як маротиба): «Шуморо X даъват кард»."""
    if db.execute("SELECT 1 FROM invited_msg WHERE user_id=?", (member,)).fetchone():
        return
    r = db.execute("SELECT owner_id FROM joins WHERE member_id=?", (member,)).fetchone()
    if not r:
        return
    who = public_name(r[0], member)
    ok = send(member, tr(member, "invited", who=who),
              markup([cb(tr(member, "btn_getlink"), "getlink")],
                     [cb(tr(member, "btn_home"), "menu")]))
    if ok:
        db.execute("INSERT OR IGNORE INTO invited_msg VALUES(?)", (member,))
        db.commit()


# ======================= Отзывы =======================

REVIEW_CAPTION = ("🎉 Ещё один человек стал владельцем аккаунта!\n\n"
                  f"Хочешь так же? Забирай ссылку в боте 👉 @{BOT_USERNAME}\n\n"
                  "🎉 Боз як нафар соҳиби аккаунт шуд!\n"
                  f"Ту ҳам мехоҳӣ? Истинодро дар бот бигир 👉 @{BOT_USERNAME}")


def send_photo(chat_id, file_id, caption, buttons=None):
    def _do(b):
        params = {"chat_id": chat_id, "photo": file_id, "caption": caption}
        if b:
            params["reply_markup"] = b
        return api("sendPhoto", **params)

    try:
        return _do(buttons)
    except Exception as e:
        if is_fancy(buttons):
            try:
                return _do(strip_fancy(buttons))
            except Exception as e2:
                print("send_photo error:", e2)
                return None
        print("send_photo error:", e)
        return None


def ask_review(uid, kind="normal", note=""):
    db.execute("INSERT OR IGNORE INTO review_wait(user_id, kind, note) VALUES(?,?,?)",
               (uid, kind, note))
    if kind == "winner":
        db.execute("UPDATE review_wait SET kind=?, note=? WHERE user_id=?", (kind, note, uid))
    db.commit()
    key = "review_ask_winner" if kind == "winner" else "review_ask"
    send(uid, tr(uid, key), markup([cb(tr(uid, "btn_skip"), "review_skip")]))


def winner_caption(uid, note):
    who = public_name(uid)
    c = note or "—"
    return (f"🏆 Это победитель — {who}! Он пригласил {c} человек и получил аккаунт в подарок 🎁\n\n"
            f"Хочешь стать следующим? Забирай ссылку в боте 👉 @{BOT_USERNAME}\n\n"
            f"🏆 Ин ғолиб — {who}! Ӯ {c} нафарро даъват кард ва аккаунтро тӯҳфа гирифт 🎁\n\n"
            f"Ту ҳам мехоҳӣ? Истинодро дар бот бигир 👉 @{BOT_USERNAME}")


def publish_review(rid):
    row = db.execute("SELECT user_id, file_id, status, kind, note FROM reviews WHERE id=?",
                     (rid,)).fetchone()
    if not row or row[2] != "pending":
        return False
    caption = winner_caption(row[0], row[4]) if row[3] == "winner" else REVIEW_CAPTION
    if not send_photo(CHANNEL_ID, row[1], caption):
        return False
    db.execute("UPDATE reviews SET status='published' WHERE id=?", (rid,))
    db.commit()
    send(row[0], tr(row[0], "review_published"))
    return True


def handle_review_photo(msg):
    uid = msg["from"]["id"]
    waiting = db.execute("SELECT kind, note FROM review_wait WHERE user_id=?", (uid,)).fetchone()
    if not waiting:
        if has_accounts(uid):
            send(uid, tr(uid, "review_hint"),
                 markup([cb(tr(uid, "btn_review"), "review")], back(uid)))
        else:
            text_, kb = screen_menu(uid)
            send(uid, text_, kb)
        return
    file_id = msg["photo"][-1]["file_id"]
    db.execute("DELETE FROM review_wait WHERE user_id=?", (uid,))
    kind = waiting[0] or "normal"
    note = waiting[1] or ""
    cur = db.execute("INSERT INTO reviews(user_id, file_id, ts, status, kind, note) "
                     "VALUES(?,?,?,'pending',?,?)",
                     (uid, file_id, int(time.time()), kind, note))
    rid = cur.lastrowid
    db.commit()
    if REVIEW_AUTOPUBLISH and publish_review(rid):
        send_photo(REVIEW_CHAT, file_id, f"📸 Отзыв опубликован в канале\nОт: {member_name(uid)}")
        return
    send(uid, tr(uid, "review_thanks"), markup([cb(tr(uid, "btn_home"), "menu")]))
    title = "🏆 Отзыв победителя" if kind == "winner" else "📸 Новый отзыв"
    send_photo(REVIEW_CHAT, file_id,
               f"{title}\nОт: {member_name(uid)}\n\nОпубликовать в канале?",
               markup([cb("✅ В канал", f"rv_ok:{rid}", "success"),
                       cb("❌ Отклонить", f"rv_no:{rid}", "danger")]))


# ======================= Додани аккаунт =======================

def give(uid):
    """Аккаунт(ҳо)-ро аз склад мебарорад ва мефиристад. Агар фиристодан нашавад — бозмегардонад."""
    if available(uid) <= 0:
        return 0
    if check_member(uid) is False:
        text, kb = sub_prompt(uid, "claim")
        send(uid, text, kb)
        return 0
    if verify_members(uid) > 0:
        send(uid, tr(uid, "give_updated") + status(uid))
    avail = available(uid)
    if avail <= 0:
        return 0
    rows = db.execute(
        "SELECT id, data FROM stock WHERE used_by IS NULL ORDER BY id LIMIT ?", (avail,)
    ).fetchall()
    if not rows:
        send(uid, tr(uid, "give_empty"), claim_kb(uid))
        send(ADMIN_ID, f"⚠️ Склад пуст! Пользователь {member_name(uid)} ждёт аккаунт. Добавьте: /add")
        return 0

    ids = [r[0] for r in rows]
    old = claimed(uid)
    now = int(time.time())
    for i in ids:
        db.execute("UPDATE stock SET used_by=?, used_at=? WHERE id=? AND used_by IS NULL",
                   (uid, now, i))
    db.execute("INSERT OR REPLACE INTO rewards VALUES(?,?)", (uid, old + len(rows)))
    db.commit()

    ok = send_gift(uid, "gift", [r[1] for r in rows])
    if not ok:
        marks = ",".join("?" * len(ids))
        db.execute(f"UPDATE stock SET used_by=NULL, used_at=NULL WHERE id IN ({marks})", ids)
        db.execute("INSERT OR REPLACE INTO rewards VALUES(?,?)", (uid, old))
        db.commit()
        send(ADMIN_ID, f"⚠️ Не удалось отправить аккаунт {member_name(uid)} "
                       "(возможно, бот заблокирован). Выдача отменена, аккаунт возвращён на склад.")
        return 0

    send(ADMIN_ID, f"📤 Выдан аккаунт\nКому: {member_name(uid)}\n\n" +
         "\n".join(r[1] for r in rows))
    ask_review(uid)
    left = stock_left()
    if left <= 3:
        send(ADMIN_ID, f"⚠️ В складе осталось только {left} аккаунт(ов). Добавьте: /add")
    return len(rows)


# ======================= Розыгрыш / Топи рӯз: аккаунт ба ғолиб =======================

def resolve_user(arg):
    arg = arg.strip().lstrip("@")
    if arg.isdigit():
        return int(arg)
    r = db.execute("SELECT user_id FROM profiles WHERE LOWER(username)=LOWER(?)", (arg,)).fetchone()
    return r[0] if r else None


def give_prize(uid, key="giveaway_win", kind="normal", note="", pending=False, **fmt):
    """Як аккаунт аз склад ба ғолиб. Ба ҳисоби даъватҳо таъсир намерасонад.
    pending=True: агар склад холӣ бошад ё ғолиб ботро /start накарда бошад, дар навбат мемонад."""
    row = db.execute("SELECT id, data FROM stock WHERE used_by IS NULL ORDER BY id LIMIT 1").fetchone()
    if not row:
        if pending:
            db.execute("INSERT OR IGNORE INTO pending_prize VALUES(?)", (uid,))
            db.commit()
        send(ADMIN_ID, f"⚠️ Склад пуст! Победитель {member_name(uid)} "
                       f"{'в очереди' if pending else 'не получил аккаунт'}. Добавьте: /add")
        return False
    db.execute("UPDATE stock SET used_by=?, used_at=? WHERE id=? AND used_by IS NULL",
               (uid, int(time.time()), row[0]))
    db.commit()
    ok = send_gift(uid, key, [row[1]], **fmt)
    if not ok:
        db.execute("UPDATE stock SET used_by=NULL, used_at=NULL WHERE id=?", (row[0],))
        if pending:
            db.execute("INSERT OR IGNORE INTO pending_prize VALUES(?)", (uid,))
        db.commit()
        send(ADMIN_ID, f"⚠️ {member_name(uid)} не нажал /start у бота — "
                       + ("аккаунт выдам автоматически, как только он напишет боту."
                          if pending else "аккаунт возвращён на склад."))
        return False
    db.execute("DELETE FROM pending_prize WHERE user_id=?", (uid,))
    db.commit()
    send(ADMIN_ID, f"🎉 Победитель: {member_name(uid)}\n\n{row[1]}")
    ask_review(uid, kind, note)
    left = stock_left()
    if left <= 3:
        send(ADMIN_ID, f"⚠️ В складе осталось только {left} аккаунт(ов). Добавьте: /add")
    return True


def deliver_pending(uid=None):
    """Аккаунтро ба ғолибони дар навбатмонда медиҳад (як корбар ё ҳама)."""
    if uid is not None:
        ids = [r[0] for r in db.execute("SELECT user_id FROM pending_prize WHERE user_id=?", (uid,))]
    else:
        ids = [r[0] for r in db.execute("SELECT user_id FROM pending_prize")]
    for u in ids:
        if not give_prize(u, kind="winner", pending=True):
            if stock_left() == 0:
                break


def handle_winner_cmd(admin_id, text):
    args = text.split()[1:]
    if not args:
        send(admin_id, "Использование: /winner @username или ID (несколько — через пробел)")
        return
    for a in args:
        uid = resolve_user(a)
        if not uid:
            send(admin_id, f"❌ {a}: нет в базе (должен был нажать /start)")
        elif give_prize(uid, kind="winner", note=""):
            send(admin_id, f"✅ {a}: аккаунт отправлен")


def handle_channel_post(post):
    """Агар дар канал паёми эълони ғолиби розыгрыш бошад — худкор аккаунт медиҳад."""
    if post["chat"]["id"] != CHANNEL_ID:
        return
    gw = post.get("giveaway_winners")
    if gw:
        # Розыгрыши расмии Telegram: натиҷа пас аз интихоби ғолибон
        if db.execute("SELECT 1 FROM prize_log WHERE msg_id=?", (post["message_id"],)).fetchone():
            return
        db.execute("INSERT INTO prize_log VALUES(?)", (post["message_id"],))
        db.commit()
        winners = gw.get("winners", [])
        send(ADMIN_ID, f"🎁 Розыгрыш завершён. Победителей: {gw.get('winner_count', len(winners))}, "
                       f"в списке: {len(winners)}. Выдаю аккаунты...")
        for u in winners:
            remember(u)
            give_prize(u["id"], kind="winner", note="", pending=True)
        if gw.get("winner_count", 0) > len(winners):
            send(ADMIN_ID, "⚠️ Telegram показал не всех победителей (лимит списка). "
                           "Остальным выдайте через /winner.")
        return
    text = post.get("text") or post.get("caption") or ""
    low = text.lower()
    if "розыгрыш" not in low or not any(w in low for w in ("победител", "ғолиб")):
        return
    if db.execute("SELECT 1 FROM prize_log WHERE msg_id=?", (post["message_id"],)).fetchone():
        return
    db.execute("INSERT INTO prize_log VALUES(?)", (post["message_id"],))
    db.commit()
    ids = []
    for e in post.get("entities", []) + post.get("caption_entities", []):
        if e["type"] == "text_mention":
            ids.append(e["user"]["id"])
        elif e["type"] == "mention":
            u = resolve_user(text[e["offset"]:e["offset"] + e["length"]])
            if u:
                ids.append(u)
    if not ids:
        send(ADMIN_ID, "⚠️ В посте розыгрыша не найден ни один @username из базы. "
                       "Используйте /winner @username")
        return
    for uid in dict.fromkeys(ids):
        give_prize(uid, kind="winner", note="")


def award_daily(day):
    """Ғолиби рӯзи `day`-ро муайян мекунад ва аккаунт медиҳад."""
    start, end = day_range(day)
    r = db.execute(
        "SELECT owner_id, COUNT(*) c FROM joins WHERE ts>=? AND ts<? "
        "GROUP BY owner_id ORDER BY c DESC, MAX(ts) ASC LIMIT 1", (start, end)).fetchone()
    if not r or r[1] < DAILY_MIN:
        return
    uid, c = r
    if give_prize(uid, key="daily_win", kind="winner", note=str(c), c=c):
        if ANNOUNCE_IN_CHANNEL:
            who = public_name(uid)
            send(CHANNEL_ID,
                 f"🏆 Победитель дня — {who}! Он пригласил {c} человек и получил аккаунт 🎁\n"
                 f"Хочешь стать следующим? 👉 @{BOT_USERNAME}\n\n"
                 f"🏆 Ғолиби рӯз — {who}! Ӯ {c} нафарро даъват кард ва аккаунт гирифт 🎁\n"
                 f"Ту ҳам мехоҳӣ? 👉 @{BOT_USERNAME}")


def daily_check():
    key = day_key()
    last = get_setting("last_daily")
    if last is None:
        set_setting("last_daily", key - 1)
        return
    if int(last) >= key - 1:
        return
    set_setting("last_daily", key - 1)
    award_daily(key - 1)


# ======================= Админ =======================

def show_invited(admin_id, arg=None):
    if arg:
        arg = arg.lstrip("@")
        if arg.isdigit():
            owners = [int(arg)]
        else:
            owners = [r[0] for r in db.execute(
                "SELECT user_id FROM profiles WHERE LOWER(username)=LOWER(?)", (arg,))]
        if not owners:
            send(admin_id, "Пользователь не найден.")
            return
    else:
        owners = [r[0] for r in db.execute(
            "SELECT owner_id FROM joins GROUP BY owner_id ORDER BY COUNT(*) DESC")]
        if not owners:
            send(admin_id, "Пока никто никого не пригласил.")
            return
    chunk = ""
    for o in owners:
        members = [r[0] for r in db.execute(
            "SELECT member_id FROM joins WHERE owner_id=?", (o,))]
        block = f"👤 {member_name(o)} — {len(members)} чел.\n"
        if members:
            block += "\n".join(f"   • {member_name(m)}" for m in members) + "\n"
        block += "\n"
        if len(chunk) + len(block) > 3800:
            send(admin_id, chunk)
            chunk = ""
        chunk += block
    if chunk.strip():
        send(admin_id, chunk)


def list_participants(admin_id):
    rows = db.execute(
        "SELECT l.user_id, COALESCE(p.name,''), COALESCE(p.username,''), "
        "(SELECT COUNT(*) FROM joins j WHERE j.owner_id=l.user_id) AS c, "
        "COALESCE((SELECT claimed FROM rewards r WHERE r.user_id=l.user_id),0) "
        "FROM links l LEFT JOIN profiles p ON p.user_id=l.user_id ORDER BY c DESC"
    ).fetchall()
    if not rows:
        send(admin_id, "Пока нет участников.")
        return
    total = sum(r[3] for r in rows)
    head = f"👥 Участников со ссылкой: {len(rows)}\nВсего приглашено: {total}\n"
    lines = []
    for i, (uid, name, uname, c, cl) in enumerate(rows, 1):
        who = name or str(uid)
        if uname:
            who += f" (@{uname})"
        lines.append(f"{i}. {who} — {c} чел. | акк: {cl}/{c // NEED}")
    chunk = head + "\n"
    for line in lines:
        if len(chunk) + len(line) > 3800:
            send(admin_id, chunk)
            chunk = ""
        chunk += line + "\n"
    if chunk.strip():
        send(admin_id, chunk)


def send_stats(admin_id):
    q = lambda s, a=(): db.execute(s, a).fetchone()[0]
    send(admin_id,
         "📊 Статистика\n\n"
         f"Нажали /start: {q('SELECT COUNT(*) FROM users')}\n"
         f"Получили ссылку: {q('SELECT COUNT(*) FROM links')}\n"
         f"Вступили по ссылкам: {q('SELECT COUNT(*) FROM joins')}\n"
         f"Пригласили {NEED}+: {q('SELECT COUNT(*) FROM (SELECT owner_id FROM joins GROUP BY owner_id HAVING COUNT(*)>=?)', (NEED,))}\n"
         f"Аккаунтов выдано всего: {q('SELECT COUNT(*) FROM stock WHERE used_by IS NOT NULL')}\n"
         f"📦 В складе осталось: {stock_left()}")


def show_given(admin_id, arg=None):
    params = ()
    where = "used_by IS NOT NULL"
    limit = 30
    if arg:
        arg = arg.lstrip("@")
        target = int(arg) if arg.isdigit() else resolve_user(arg)
        if not target:
            send(admin_id, "Пользователь не найден.")
            return
        where += " AND used_by=?"
        params = (target,)
    rows = db.execute(
        f"SELECT used_by, data, used_at FROM stock WHERE {where} "
        "ORDER BY COALESCE(used_at,0) DESC, id DESC LIMIT ?", params + (limit,)).fetchall()
    if not rows:
        send(admin_id, "Выданных аккаунтов нет.")
        return
    chunk = f"📤 Последние выданные (до {limit}):\n\n"
    for uid, data, ts in rows:
        when = time.strftime("%d.%m.%Y %H:%M", time.gmtime(ts + TZ_OFFSET)) if ts else "—"
        block = f"👤 {member_name(uid)}\n🕒 {when}\n{data}\n\n"
        if len(chunk) + len(block) > 3800:
            send(admin_id, chunk)
            chunk = ""
        chunk += block
    if chunk.strip():
        send(admin_id, chunk)


def add_stock(text):
    """Аккаунтҳоро ба склад илова мекунад. Агар сатри холӣ бошад — блокҳо; вагарна ҳар сатр як аккаунт."""
    text = text.replace("\r", "").strip()
    parts = [p.strip() for p in (text.split("\n\n") if "\n\n" in text else text.split("\n"))]
    parts = [p for p in parts if p]
    for p in parts:
        db.execute("INSERT INTO stock(data) VALUES(?)", (p,))
    db.commit()
    return len(parts)


_EMO = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF\u203C\u2049\u2139]\ufe0f?")


def used_emojis():
    """Ҳамаи эмодзиҳое, ки бот истифода мебарад (матн ва тугмаҳо)."""
    found = []
    pool = [v for lang in S.values() for v in lang.values()]
    pool += ["📧🔑🕒📋🧪📊👥🔗📤⚙️➕📖"]
    for t in pool:
        for m in _EMO.finditer(t):
            e = norm_emoji(m.group(0))
            if e not in found:
                found.append(e)
    return found


def custom_emojis(msg):
    """Рӯйхати (эмодзӣ, custom_emoji_id) аз паём. Offset-ҳои Telegram — UTF-16."""
    text = msg.get("text") or msg.get("caption") or ""
    ents = (msg.get("entities") or []) + (msg.get("caption_entities") or [])
    t16 = text.encode("utf-16-le")
    out = []
    for e in ents:
        if e.get("type") == "custom_emoji":
            ch = t16[e["offset"] * 2:(e["offset"] + e["length"]) * 2].decode("utf-16-le", "ignore")
            out.append((norm_emoji(ch), e["custom_emoji_id"]))
    return out


def emoji_pairs(msg):
    """Ҷуфтҳо (эмодзии оддӣ, custom_emoji_id).
    «🎁 = <премиум>» -> 🎁 ба премиум пайваст мешавад. Агар эмодзии оддӣ набошад, худи аломати премиум."""
    text = msg.get("text") or msg.get("caption") or ""
    ents = sorted([e for e in (msg.get("entities") or []) + (msg.get("caption_entities") or [])
                   if e.get("type") == "custom_emoji"], key=lambda e: e["offset"])
    t16 = text.encode("utf-16-le")
    pairs, prev = [], 0
    for e in ents:
        seg = t16[prev * 2:e["offset"] * 2].decode("utf-16-le", "ignore")
        toks = [t for t in re.split(r"[\s=:→>\-]+", seg) if t and not t.startswith("/")]
        end = e["offset"] + e["length"]
        fallback = t16[e["offset"] * 2:end * 2].decode("utf-16-le", "ignore")
        pairs.append((norm_emoji(toks[-1] if toks else fallback), e["custom_emoji_id"]))
        prev = end
    return pairs


def download_file(file_id):
    path = api("getFile", file_id=file_id)["file_path"]
    with urllib.request.urlopen(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{path}", timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def send_test_card(uid):
    """Корти намунавӣ ба админ (склад ва ҳисобҳо тағйир намеёбанд)."""
    send_gift(uid, "gift", ["test.user@gmail.com:Pass12345"])
    send_gift(uid, "gift", ["first@gmail.com:Pass111", "second@gmail.com:Pass222"])


ADMIN_HELP = ("⚙️ Админ-команды\n\n"
              "/add — добавить аккаунты (следующим сообщением или .txt файлом)\n"
              "/stats — статистика\n"
              "/users — участники\n"
              "/invited [@user|ID] — кого пригласили\n"
              "/given [@user|ID] — кому выдано\n"
              "/winner @user [@user2] — выдать аккаунт победителю розыгрыша\n"
              "/promo — каналы: реклама и задания «пригласи N — получи аккаунт»\n"
              "/test — тест красивой карточки аккаунта\n"
              "/emoji 🎁 <custom_emoji_id> — премиум-эмодзи для кнопок\n"
              "/emoji — раздел премиум-эмодзи, /emoji clear — сбросить, /emoji del 🎁 — удалить\n"
              "Проще всего: «🎁 = премиум-эмодзи» (обычный эмодзи, знак равно, премиум)")


# ======================= Каналы: реклама и задания (админ выбирает) =======================

PROMO_MAX = 8
CAMP_NEED_DEFAULT = NEED
_BOT = {}
PROMO_COLS = "id, title, url, active, icon, fb, chat_id, need"


def bot_id():
    if "id" not in _BOT:
        _BOT["id"] = api("getMe")["id"]
    return _BOT["id"]


def bot_is_admin(chat_id):
    try:
        r = api("getChatMember", chat_id=chat_id, user_id=bot_id())
        return r["status"] in ("administrator", "creator")
    except Exception as e:
        print("bot_is_admin error:", e)
        return False


def promo_list(active_only=False):
    q = f"SELECT {PROMO_COLS} FROM promo_channels"
    if active_only:
        q += " WHERE active=1"
    return db.execute(q + " ORDER BY id").fetchall()


def promo_get(cid):
    return db.execute(f"SELECT {PROMO_COLS} FROM promo_channels WHERE id=?", (cid,)).fetchone()


def is_camp(row):
    """Канал-задание: chat_id маълум ва need > 0."""
    return bool(row and row[6] and (row[7] or 0) > 0)


def promo_button(title, url, icon=None, fb=None, data=None):
    if icon:
        FALLBACK[(title, icon)] = fb or ""
        b = {"text": title, "icon_custom_emoji_id": icon}
        b.update({"callback_data": data} if data else {"url": url})
        return b
    return cb(title, data) if data else url_btn(title, url)


def promo_rows():
    return [[promo_button(r[1], r[2], r[4], r[5], f"camp:{r[0]}" if is_camp(r) else None)]
            for r in promo_list(True)]


def promo_on(key):
    return get_setting(key, "1") == "1"


def send_promo(uid):
    """Баъди тӯҳфа: тугмаҳои каналҳо/заданияҳо."""
    if not promo_on("promo_gift"):
        return
    rows = promo_rows()
    if rows:
        send(uid, tr(uid, "promo_after"), markup(*rows))


# ---- ҳисобҳои задание ----

def c_count(cid, uid):
    return db.execute("SELECT COUNT(*) FROM c_joins WHERE camp_id=? AND owner_id=?",
                      (cid, uid)).fetchone()[0]


def c_claimed(cid, uid):
    r = db.execute("SELECT claimed FROM c_rewards WHERE camp_id=? AND user_id=?", (cid, uid)).fetchone()
    return r[0] if r else 0


def c_avail(row, uid):
    return max(0, c_count(row[0], uid) // row[7] - c_claimed(row[0], uid))


def c_progress(row, uid):
    """(k, bar): пешрафт дар даври ҷорӣ."""
    n, need = c_count(row[0], uid), row[7]
    k = n % need
    if k == 0 and n > 0 and c_avail(row, uid) > 0:
        k = need
    return k, "▓" * k + "░" * (need - k)


def get_clink(user, row):
    uid, cid = user["id"], row[0]
    r = db.execute("SELECT link FROM c_links WHERE camp_id=? AND user_id=?", (cid, uid)).fetchone()
    if r:
        return r[0]
    name = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or str(uid)
    link = api("createChatInviteLink", chat_id=row[6], name=name[:32])["invite_link"]
    db.execute("INSERT OR REPLACE INTO c_links VALUES(?,?,?)", (cid, uid, link))
    db.commit()
    return link


def c_verify(row, owner):
    for (m,) in db.execute("SELECT member_id FROM c_joins WHERE camp_id=? AND owner_id=?",
                           (row[0], owner)).fetchall():
        if check_member(m, row[6]) is False:
            db.execute("DELETE FROM c_joins WHERE camp_id=? AND member_id=?", (row[0], m))
    db.commit()


def screen_camp(user, cid):
    uid = user["id"]
    row = promo_get(cid)
    if not row or not row[3] or not is_camp(row):
        return tr(uid, "camp_closed"), markup(back(uid))
    try:
        link = get_clink(user, row)
    except Exception as e:
        print("get_clink error:", e)
        send(ADMIN_ID, f"⚠️ Не удалось создать ссылку для канала «{row[1]}». "
                       "Проверьте: бот должен быть админом канала с правом приглашать пользователей.")
        return (tr(uid, "link_fail"), markup([cb(tr(uid, "btn_retry"), f"camp:{cid}")], back(uid)))
    k, bar = c_progress(row, uid)
    avail = c_avail(row, uid)
    text = tr(uid, "camp_text", title=row[1], need=row[7], link=link, bar=bar, n=k,
              total=c_count(cid, uid), got=c_claimed(cid, uid), avail=avail)
    rows = []
    if avail > 0:
        rows.append([cb(tr(uid, "btn_claim"), f"campclaim:{cid}", "success")])
    share = ("https://t.me/share/url?url=" + urllib.parse.quote(link)
             + "&text=" + urllib.parse.quote(tr(uid, "camp_share", title=row[1])))
    rows.append([url_btn(tr(uid, "btn_share"), share)])
    rows.append([url_btn(tr(uid, "btn_open_ch"), row[2])])
    rows.append(back(uid))
    return text, markup(*rows)


def claim_camp(uid, cid, verify=True):
    row = promo_get(cid)
    if not row or not row[3] or not is_camp(row):
        return 0
    if verify:
        c_verify(row, uid)
    given = 0
    while c_avail(row, uid) > 0:
        ok = give_prize(uid, key="camp_win", kind="normal",
                        title=html.escape(row[1]), c=c_count(cid, uid))
        if not ok:
            break
        db.execute("INSERT OR REPLACE INTO c_rewards VALUES(?,?,?)", (cid, uid, c_claimed(cid, uid) + 1))
        db.commit()
        given += 1
    if given == 0 and c_avail(row, uid) > 0:
        send(uid, tr(uid, "give_empty"),
             markup([cb(tr(uid, "btn_claim"), f"campclaim:{cid}", "success")], back(uid)))
    return given


def handle_camp_member(cm):
    """Вурод/хуруҷ дар каналҳои-задание: ҳисоби даъватҳо ва додани аккаунт."""
    chat_id = cm["chat"]["id"]
    row = db.execute(f"SELECT {PROMO_COLS} FROM promo_channels WHERE chat_id=? "
                     "ORDER BY active DESC, id LIMIT 1", (chat_id,)).fetchone()
    if not row:
        return
    cid = row[0]
    new, old = cm["new_chat_member"], cm["old_chat_member"]
    user = new["user"]
    member = user["id"]
    was_in = old["status"] in ("member", "administrator", "creator") or \
        (old["status"] == "restricted" and old.get("is_member", False))
    now_in = new["status"] in ("member", "administrator", "creator") or \
        (new["status"] == "restricted" and new.get("is_member", False))
    if was_in and not now_in:
        db.execute("DELETE FROM c_joins WHERE camp_id=? AND member_id=?", (cid, member))
        db.commit()
        return
    if not now_in or was_in or not row[3] or not is_camp(row):
        return
    inv = (cm.get("invite_link") or {}).get("invite_link")
    if not inv:
        return
    r = db.execute("SELECT user_id FROM c_links WHERE camp_id=? AND link=?", (cid, inv)).fetchone()
    if not r:
        return
    owner = r[0]
    if owner == member:
        return
    if db.execute("SELECT 1 FROM c_joins WHERE camp_id=? AND member_id=?", (cid, member)).fetchone():
        return
    remember(user)
    db.execute("INSERT OR IGNORE INTO c_joins(camp_id, owner_id, member_id, ts) VALUES(?,?,?,?)",
               (cid, owner, member, int(time.time())))
    db.commit()
    k, bar = c_progress(row, owner)
    send(owner, tr(owner, "camp_new_member", title=row[1], bar=bar, n=k, need=row[7]),
         markup([cb(tr(owner, "btn_home"), "menu")]))
    if c_avail(row, owner) > 0:
        claim_camp(owner, cid, verify=False)


# ---- админ: иловаи канал ----

def fwd_chat(msg):
    fo = msg.get("forward_origin")
    if fo and fo.get("type") == "channel" and fo.get("chat"):
        return fo["chat"]
    fc = msg.get("forward_from_chat")
    if fc and fc.get("type") == "channel":
        return fc
    return None


def normalize_url(tok):
    tok = tok.strip().rstrip(".,;)")
    if tok.startswith("@"):
        tok = "https://t.me/" + tok[1:]
    elif tok.lower().startswith(("t.me/", "www.t.me/")):
        tok = "https://" + tok
    p = urllib.parse.urlparse(tok)
    return tok if p.scheme in ("http", "https") and p.netloc else None


def chat_ref_from_url(url):
    parts = [x for x in urllib.parse.urlparse(url).path.split("/") if x]
    if not parts:
        return None
    if parts[0] == "c" and len(parts) > 1 and parts[1].isdigit():
        return int("-100" + parts[1])
    if parts[0].startswith("+") or parts[0] == "joinchat":
        return None
    return "@" + parts[0]


def parse_promo(msg):
    """Паём -> (title, url, icon_id, fallback_emoji). Эмодзии премиум дар аввал = иконкаи тугма."""
    text = msg.get("text") or msg.get("caption") or ""
    icon = fb = None
    ents = [e for e in (msg.get("entities") or []) if e.get("type") == "custom_emoji" and e["offset"] == 0]
    if ents:
        t16 = text.encode("utf-16-le")
        n = ents[0]["length"]
        fb = t16[:n * 2].decode("utf-16-le", "ignore")
        icon = ents[0]["custom_emoji_id"]
        text = t16[n * 2:].decode("utf-16-le", "ignore")
    m = re.search(r"(https?://\S+|(?:www\.)?t\.me/\S+|@[A-Za-z0-9_]{4,})", text)
    if not m:
        return None
    url = normalize_url(m.group(0))
    if not url:
        return None
    title = (text[:m.start()] + " " + text[m.end():]).strip(" \n\t=-—:|")
    title = re.sub(r"\s+", " ", title)
    if not title:
        title = "Канал " + url.rstrip("/").rsplit("/", 1)[-1]
        if not icon:
            title = "📢 " + title
    return title[:40], url, icon, fb


def try_enable_camp(cid):
    """Канали реклама-ро ба вазифа табдил медиҳад: chat_id-ро аз истинод муайян мекунад."""
    row = promo_get(cid)
    ref = chat_ref_from_url(row[2]) if row and row[2] else None
    if ref is None:
        return False
    try:
        chat = api("getChat", chat_id=ref)
    except Exception as e:
        print("try_enable_camp error:", e)
        return False
    db.execute("UPDATE promo_channels SET chat_id=?, need=CASE WHEN COALESCE(need,0)>0 THEN need ELSE ? END "
               "WHERE id=?", (chat["id"], CAMP_NEED_DEFAULT, cid))
    db.commit()
    return True


def migrate_promos():
    """Ҳангоми оғоз: каналҳои реклама-и кӯҳна (бе chat_id) худкор ба вазифа табдил меёбанд."""
    for r in promo_list():
        if not r[6] and try_enable_camp(r[0]):
            send(ADMIN_ID, f"🎯 Канал «{r[1]}» автоматически переведён в режим задания "
                           f"({CAMP_NEED_DEFAULT} чел. = 1 аккаунт). Бот должен быть админом канала.")


def handle_promo_add(uid, msg):
    target = get_setting("promo_target")
    if target:
        fc_ = fwd_chat(msg)
        if not fc_:
            send(uid, "❌ Перешлите сюда любой пост из канала (или нажмите «Отмена» в сообщении выше).")
            return
        db.execute("UPDATE promo_channels SET chat_id=?, need=CASE WHEN COALESCE(need,0)>0 THEN need ELSE ? END "
                   "WHERE id=?", (fc_["id"], CAMP_NEED_DEFAULT, int(target)))
        db.commit()
        set_setting("promo_target", "")
        set_setting("promo_mode", 0)
        send(uid, "✅ Задание включено. Не забудьте сделать бота админом канала "
                  "(право «Приглашать пользователей»).")
        t_, kb_ = screen_promo_item(int(target))
        send(uid, t_, kb_)
        return
    text = msg.get("text") or msg.get("caption") or ""
    icon = fb = url = title = None
    chat = None
    fc = fwd_chat(msg)
    if fc:
        chat = fc
        title = ("📢 " + (fc.get("title") or "Канал"))[:40]
        if fc.get("username"):
            url = "https://t.me/" + fc["username"]
    else:
        res = parse_promo(msg)
        idm = re.search(r"-100\d{6,}", text)
        if not res and not idm:
            send(uid, "❌ Не нашёл ссылку. Отправьте, например: 🔥 SSM SHOP https://t.me/ssmshop, "
                      "@ssmshop или перешлите пост из канала.")
            return
        if res:
            title, url, icon, fb = res
        ref = chat_ref_from_url(url) if url else None
        if ref is None and idm:
            ref = int(idm.group(0))
        if ref is not None:
            try:
                chat = api("getChat", chat_id=ref)
            except Exception as e:
                print("getChat error:", e)
        if not title and chat:
            title = ("📢 " + (chat.get("title") or "Канал"))[:40]
    chat_id = chat["id"] if chat else None
    if not url and chat_id:
        if chat.get("username"):
            url = "https://t.me/" + chat["username"]
        else:
            try:
                url = api("exportChatInviteLink", chat_id=chat_id)
                if not isinstance(url, str):
                    url = None
            except Exception as e:
                print("exportChatInviteLink error:", e)
    if not url or not title:
        send(uid, "❌ Не удалось получить ссылку канала. Отправьте ссылку вместе с названием "
                  "или сделайте бота админом и перешлите пост из канала.")
        return
    if len(promo_list()) >= PROMO_MAX:
        set_setting("promo_mode", 0)
        send(uid, f"⚠️ Максимум {PROMO_MAX} каналов. Удалите лишний.")
        return
    cur = db.execute("INSERT INTO promo_channels(title, url, active, icon, fb, chat_id, need) "
                     "VALUES(?,?,1,?,?,?,?)",
                     (title, url, icon, fb, chat_id, CAMP_NEED_DEFAULT if chat_id else 0))
    db.commit()
    set_setting("promo_mode", 0)
    if chat_id and bot_is_admin(chat_id):
        note = f"🎯 Задание включено: {CAMP_NEED_DEFAULT} человек в этот канал = 1 аккаунт."
    elif chat_id:
        note = ("⚠️ Бот пока не админ в этом канале. Сделайте бота админом (право «Приглашать "
                "пользователей»), иначе личные ссылки не создадутся.")
    else:
        note = ("📣 Добавлен как обычная реклама (без задания). Чтобы включить задание «пригласи — "
                "получи аккаунт»: удалите и добавьте снова, переслав пост из канала "
                "(бот должен быть админом канала).")
    send(uid, "✅ Канал добавлен\n" + note)
    t_, kb_ = screen_promo_item(cur.lastrowid)
    send(uid, t_, kb_)


def screen_promo_admin():
    rows = promo_list()
    lines = ["📢 Каналы: реклама и задания", "",
             "🎯 Задание: пользователь приглашает N человек в канал по личной ссылке и получает аккаунт.",
             "📣 Реклама: просто кнопка со ссылкой.", ""]
    if rows:
        lines.append(f"Каналы ({len(rows)}/{PROMO_MAX}):")
        for i, r in enumerate(rows, 1):
            mode = f"🎯 {r[7]} чел." if is_camp(r) else "📣"
            lines.append(f"{i}. {'✅' if r[3] else '⏸'} {mode} {(r[5] + ' ') if r[4] and r[5] else ''}{r[1]}")
    else:
        lines.append("Каналов пока нет. Нажмите «➕ Добавить канал».")
    lines += ["", "Где показывать кнопки:",
              f"• В главном меню: {'✅' if promo_on('promo_menu') else '❌'}",
              f"• После выдачи подарка: {'✅' if promo_on('promo_gift') else '❌'}"]
    kb = []
    for r in rows:
        kb.append([cb(f"{'✅' if r[3] else '⏸'} {'🎯' if is_camp(r) else '📣'} {r[1][:24]}", f"pr:o:{r[0]}")])
    kb.append([cb(f"Меню: {'✅' if promo_on('promo_menu') else '❌'}", "pr:menu"),
               cb(f"После подарка: {'✅' if promo_on('promo_gift') else '❌'}", "pr:gift")])
    if len(rows) < PROMO_MAX:
        kb.append([cb("➕ Добавить канал", "pr:add")])
    kb.append([cb("⬅️ Админ-панель", "admin")])
    return "\n".join(lines), markup(*kb)


def screen_promo_item(cid):
    row = promo_get(cid)
    if not row:
        return screen_promo_admin()
    _, title, url, active, icon, fb, chat_id, need = row
    lines = [f"📢 {title}", f"Ссылка: {url}"]
    if is_camp(row):
        joined = db.execute("SELECT COUNT(*) FROM c_joins WHERE camp_id=?", (cid,)).fetchone()[0]
        given = db.execute("SELECT COALESCE(SUM(claimed),0) FROM c_rewards WHERE camp_id=?", (cid,)).fetchone()[0]
        adm = bot_is_admin(chat_id)
        lines += [f"Режим: 🎯 задание — {need} чел. = 1 аккаунт",
                  "Бот админ в канале: " + ("✅" if adm else "❌ (сделайте админом с правом приглашать)"),
                  f"Вступило по заданию: {joined}",
                  f"Выдано аккаунтов: {given}"]
    else:
        lines += ["Режим: 📣 только реклама — кнопка ведёт просто в канал, ссылки для приглашения нет.",
                  "Нажмите «🎯 Включить задание»: пользователь получит личную ссылку, а бот будет "
                  "считать приглашённых (бот должен быть админом канала)."]
    lines.append("Статус: " + ("✅ включён" if active else "⏸ выключен"))
    kb = [[cb("⏸ Выключить" if active else "✅ Включить", f"pr:t:{cid}"),
           cb("🗑 Удалить", f"pr:d:{cid}", "danger")]]
    if is_camp(row):
        kb.append([cb(f"• {v} •" if v == need else str(v), f"pr:n:{cid}:{v}") for v in (3, 5, 10, 15)])
        kb.append([cb("🔄 Проверить права", f"pr:o:{cid}")])
    if not is_camp(row):
        kb.insert(1, [cb("🎯 Включить задание", f"pr:e:{cid}", "success")])
    kb.append([cb("⬅️ Каналы", "adm:promo")])
    return "\n".join(lines), markup(*kb)


def screen_promo_add():
    return ("➕ Добавить канал\n\n"
            "Отправьте ОДНО из:\n"
            "• ссылку с названием: 🔥 SSM SHOP https://t.me/ssmshop (или просто @ssmshop)\n"
            "• пересланный пост из канала (подходит и для приватных каналов)\n\n"
            "Чтобы работало задание «пригласи N человек — получи аккаунт», сделайте бота админом "
            "канала с правом «Приглашать пользователей».\n"
            "Если канал не определился — он добавится как обычная реклама.\n\n"
            "Премиум-эмодзи в самом начале названия станет иконкой кнопки.",
            markup([cb("Отмена", "pr:cancel")]))


def clear_emoji():
    db.execute("DELETE FROM emoji_map")
    db.commit()
    EMOJI_MAP.clear()
    save_emoji_backup()


def screen_emoji():
    """Бахши «Премиум-эмодзи» дар панели админ."""
    used = used_emojis()
    missing = [e for e in used if e not in EMOJI_MAP]
    done = [e for e in used if e in EMOJI_MAP] + [e for e in EMOJI_MAP if e not in used]
    text = ("✨ Премиум-эмодзи (в кнопках и в тексте)\n\n"
            "Отправь /emoji и премиум-эмодзи (из любого набора). Формат:\n"
            "/emoji\n🎁 = (премиум)\n🏠 = (премиум)\n\n"
            "Слева — обычный эмодзи, справа — премиум, который его заменит. "
            "Если у премиум-эмодзи тот же базовый смайл, можно отправить его без «=».\n\n"
            f"Ещё не настроены ({len(missing)}): " + (" ".join(missing) if missing else "—") + "\n"
            f"Уже настроены ({len(done)}): " + (" ".join(done) if done else "—") + "\n\n"
            "/emoji clear — сбросить всё.\n"
            "⚠️ Работает, если у владельца бота есть Telegram Premium. "
            "Если Telegram откажет, бот сам покажет обычные эмодзи.")
    return text, markup([cb("🔄 Обновить", "adm:emoji")],
                        [cb("🗑 Сбросить всё", "adm:emoji_ask", "danger")],
                        [cb("⬅️ Админ-панель", "admin")])


def screen_emoji_confirm():
    return (f"🗑 Сбросить все премиум-эмодзи ({len(EMOJI_MAP)})?\n\n"
            "Кнопки и текст вернутся к обычным эмодзи.",
            markup([cb("✅ Да, сбросить", "adm:emoji_clear", "danger"),
                    cb("Отмена", "adm:emoji")]))


def screen_admin():
    return (f"⚙️ Админ-панель\n\n📦 В складе: {stock_left()}\n🔖 Версия: {BOT_VERSION}",
            markup([cb("📊 Статистика", "adm:stats"), cb("👥 Участники", "adm:users")],
                   [cb("🔗 Приглашения", "adm:inv"), cb("📤 Выдано", "adm:given")],
                   [cb("➕ Добавить аккаунты", "adm:add"), cb("📖 Команды", "adm:help")],
                   [cb("✨ Премиум-эмодзи", "adm:emoji"), cb("🧪 Тест карточки", "adm:test")],
                   [cb("📢 Каналы и задания", "adm:promo")],
                   [cb("⬅️ Меню", "menu")]))


# ======================= Коркарди update-ҳо =======================

def handle_chat_member(cm):
    """Вурод/хуруҷи узвҳо дар канал: ҳисоби даъватҳо."""
    if cm["chat"]["id"] != CHANNEL_ID:
        return
    new = cm["new_chat_member"]
    old = cm["old_chat_member"]
    user = new["user"]
    member = user["id"]
    was_in = old["status"] in ("member", "administrator", "creator") or \
        (old["status"] == "restricted" and old.get("is_member", False))
    now_in = new["status"] in ("member", "administrator", "creator") or \
        (new["status"] == "restricted" and new.get("is_member", False))

    if was_in and not now_in:
        db.execute("DELETE FROM joins WHERE member_id=?", (member,))
        db.commit()
        return
    if not now_in or was_in:
        return

    inv = (cm.get("invite_link") or {}).get("invite_link")
    if not inv:
        return
    row = db.execute("SELECT user_id FROM links WHERE link=?", (inv,)).fetchone()
    if not row:
        return
    owner = row[0]
    if owner == member:
        return
    if db.execute("SELECT 1 FROM joins WHERE member_id=?", (member,)).fetchone():
        return
    remember(user)
    db.execute("INSERT OR IGNORE INTO joins(owner_id, member_id, ts) VALUES(?,?,?)",
               (owner, member, int(time.time())))
    db.commit()

    cnt = count(owner)
    if cnt % NEED == 0:
        send(owner, tr(owner, "congrats", c=cnt))
    kb_rows = []
    if available(owner) > 0:
        kb_rows.append([cb(tr(owner, "btn_claim"), "claim", "success")])
    kb_rows.append([cb(tr(owner, "btn_home"), "menu")])
    send(owner, tr(owner, "new_member", status=status(owner)), markup(*kb_rows))
    notify_invited(member)


def handle_message(msg):
    if msg["chat"]["type"] != "private" or "from" not in msg:
        return
    user = msg["from"]
    uid = user["id"]
    if user.get("is_bot"):
        return
    db.execute("INSERT OR IGNORE INTO users VALUES(?)", (uid,))
    db.commit()
    remember(user)
    if db.execute("SELECT 1 FROM pending_prize WHERE user_id=?", (uid,)).fetchone():
        deliver_pending(uid)

    if uid == ADMIN_ID and get_setting("promo_mode") == "1":
        _t = (msg.get("text") or msg.get("caption") or "")
        if fwd_chat(msg) or (_t and not _t.startswith("/")):
            handle_promo_add(uid, msg)
            return

    if "photo" in msg:
        handle_review_photo(msg)
        return

    text = (msg.get("text") or "").strip()

    if uid == ADMIN_ID:
        doc = msg.get("document")
        if doc and (doc.get("file_name") or "").lower().endswith(".txt"):
            try:
                n = add_stock(download_file(doc["file_id"]))
                set_setting("add_mode", 0)
                send(uid, f"✅ Добавлено аккаунтов: {n}\n📦 В складе: {stock_left()}")
                deliver_pending()
            except Exception as e:
                send(uid, f"❌ Не удалось прочитать файл: {e}")
            return
        if get_setting("add_mode") == "1" and text and not text.startswith("/"):
            n = add_stock(text)
            set_setting("add_mode", 0)
            send(uid, f"✅ Добавлено аккаунтов: {n}\n📦 В складе: {stock_left()}")
            deliver_pending()
            return

    if uid == ADMIN_ID:
        ces = emoji_pairs(msg)
        if ces:
            if text.lower().startswith("/emoji") or "=" in text:
                for ch, cid in ces:
                    db.execute("INSERT OR REPLACE INTO emoji_map VALUES(?,?)", (ch, cid))
                    EMOJI_MAP[ch] = cid
                db.commit()
                save_emoji_backup()
                send(uid, "✅ Сохранено: " + " ".join(c for c, _ in ces))
                t_, kb_ = screen_emoji()
                send(uid, t_, kb_)
            else:
                send(uid, "ID премиум-эмодзи:\n" + "\n".join(f"{c} → {i}" for c, i in ces)
                     + "\n\nЧтобы сохранить для кнопок, отправьте: 🎁 = премиум-эмодзи "
                       "(можно несколько: 🎁 = ⭐ 📦 = ⭐).")
            return

    if not text:
        return
    parts = text.split(maxsplit=1)
    cmd = parts[0].split("@")[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""

    if cmd == "/start":
        if not has_lang(uid):
            send(uid, tr(uid, "lang_prompt"), lang_kb("s"))
        else:
            t, kb = screen_menu(uid, welcome=True)
            send(uid, t, kb)
        return
    if cmd in ("/menu", "/help"):
        t, kb = screen_menu(uid)
        send(uid, t, kb)
        return

    if uid != ADMIN_ID:
        t, kb = screen_menu(uid)
        send(uid, t, kb)
        return

    if cmd == "/admin":
        t, kb = screen_admin()
        send(uid, t, kb)
    elif cmd == "/add":
        if arg:
            n = add_stock(arg)
            send(uid, f"✅ Добавлено аккаунтов: {n}\n📦 В складе: {stock_left()}")
            deliver_pending()
        else:
            set_setting("add_mode", 1); set_setting("promo_mode", 0)
            send(uid, "Отправьте аккаунты одним сообщением (каждый с новой строки; "
                      "если аккаунт из нескольких строк — разделяйте аккаунты пустой строкой) "
                      "или пришлите .txt файл.")
    elif cmd == "/promo":
        t, kb = screen_promo_admin()
        send(uid, t, kb)
    elif cmd == "/version":
        send(uid, f"🔖 Версия: {BOT_VERSION}")
    elif cmd == "/test":
        send_test_card(uid)
    elif cmd == "/stats":
        send_stats(uid)
    elif cmd == "/users":
        list_participants(uid)
    elif cmd == "/invited":
        show_invited(uid, arg or None)
    elif cmd == "/given":
        show_given(uid, arg or None)
    elif cmd == "/winner":
        handle_winner_cmd(uid, text)
    elif cmd == "/emoji":
        p = arg.split()
        if not p:
            t_, kb_ = screen_emoji()
            send(uid, t_, kb_)
        elif p[0].lower() == "clear":
            clear_emoji()
            send(uid, "✅ Все премиум-эмодзи сброшены")
        elif p[0].lower() == "missing":
            miss = [e for e in used_emojis() if e not in EMOJI_MAP]
            send(uid, ("Ещё обычные (без премиума):\n" + " ".join(miss) +
                       "\n\nОтправьте пары, например:\n🏠 = <премиум> 📦 = <премиум>") if miss
                 else "✅ Все эмодзи уже премиум")
        elif p and p[0].lower() == "list":
            send(uid, "Премиум-эмодзи:\n" + ("\n".join(f"{e} → {c}" for e, c in EMOJI_MAP.items())
                                             or "пусто"))
        elif len(p) == 2 and p[0].lower() == "del":
            db.execute("DELETE FROM emoji_map WHERE emoji=?", (norm_emoji(p[1]),))
            db.commit()
            EMOJI_MAP.pop(norm_emoji(p[1]), None)
            save_emoji_backup()
            send(uid, "✅ Удалено")
        elif len(p) == 2:
            db.execute("INSERT OR REPLACE INTO emoji_map VALUES(?,?)", (norm_emoji(p[0]), p[1]))
            db.commit()
            EMOJI_MAP[norm_emoji(p[0])] = p[1]
            save_emoji_backup()
            send(uid, "✅ Сохранено")
        else:
            t_, kb_ = screen_emoji()
            send(uid, t_, kb_)
    else:
        send(uid, ADMIN_HELP)


def handle_callback(cq):
    user = cq["from"]
    uid = user["id"]
    data = cq.get("data", "")
    try:
        api("answerCallbackQuery", callback_query_id=cq["id"])
    except Exception:
        pass
    m = cq.get("message")
    if not m:
        return
    chat_id = m["chat"]["id"]
    mid = m["message_id"]
    db.execute("INSERT OR IGNORE INTO users VALUES(?)", (uid,))
    db.commit()
    remember(user)

    if data == "menu":
        show(chat_id, mid, screen_menu(uid))
    elif data == "lang":
        show(chat_id, mid, (tr(uid, "lang_prompt"), lang_kb("m", uid)))
    elif data.startswith("lang:"):
        _, code, mode = data.split(":")
        if code in S:
            set_lang(uid, code)
        show(chat_id, mid, screen_menu(uid, welcome=(mode == "s")))
    elif data == "help":
        show(chat_id, mid, screen_help(uid))
    elif data == "progress":
        show(chat_id, mid, screen_progress(uid))
    elif data == "top":
        show(chat_id, mid, screen_top(uid))
    elif data == "today":
        show(chat_id, mid, screen_today(uid))
    elif data == "myacc":
        show(chat_id, mid, screen_archive(uid, 0))
    elif data.startswith("acc:"):
        show(chat_id, mid, screen_archive(uid, int(data.split(":")[1])))
    elif data == "getlink":
        show(chat_id, mid, screen_link(user))
    elif data == "promo":
        show(chat_id, mid, screen_promo(user))
    elif data.startswith("camp:"):
        show(chat_id, mid, screen_camp(user, int(data.split(":")[1])))
    elif data.startswith("campclaim:"):
        cid_ = int(data.split(":")[1])
        claim_camp(uid, cid_)
        show(chat_id, mid, screen_camp(user, cid_))
    elif data == "claim":
        if available(uid) > 0:
            give(uid)
        else:
            cnt = count(uid)
            if cnt // NEED > 0:
                t = tr(uid, "claim_all", r=NEED - cnt % NEED)
            else:
                t = tr(uid, "claim_need", c=cnt, need=NEED, r=NEED - cnt)
            show(chat_id, mid, (t, markup([cb(tr(uid, "btn_link"), "getlink")], back(uid))))
    elif data == "review":
        if has_accounts(uid):
            ask_review(uid)
        else:
            send(uid, tr(uid, "review_after_only"))
    elif data == "review_skip":
        db.execute("DELETE FROM review_wait WHERE user_id=?", (uid,))
        db.commit()
        show(chat_id, mid, screen_menu(uid))
    elif uid == ADMIN_ID and data == "admin":
        show(chat_id, mid, screen_admin())
    elif uid == ADMIN_ID and data.startswith("adm:"):
        act = data.split(":")[1]
        if act == "stats":
            send_stats(uid)
        elif act == "users":
            list_participants(uid)
        elif act == "inv":
            show_invited(uid)
        elif act == "given":
            show_given(uid)
        elif act == "test":
            send_test_card(uid)
        elif act == "promo":
            show(chat_id, mid, screen_promo_admin())
        elif act == "emoji":
            show(chat_id, mid, screen_emoji())
        elif act == "emoji_ask":
            show(chat_id, mid, screen_emoji_confirm())
        elif act == "emoji_clear":
            clear_emoji()
            show(chat_id, mid, screen_emoji())
        elif act == "help":
            send(uid, ADMIN_HELP)
        elif act == "add":
            set_setting("add_mode", 1); set_setting("promo_mode", 0)
            send(uid, "Отправьте аккаунты одним сообщением или .txt файлом.")
    elif uid == ADMIN_ID and data.startswith("pr:"):
        parts = data.split(":")
        act = parts[1]
        if act == "o":
            show(chat_id, mid, screen_promo_item(int(parts[2])))
            return
        if act == "e":
            cid_ = int(parts[2])
            if try_enable_camp(cid_):
                show(chat_id, mid, screen_promo_item(cid_))
            else:
                set_setting("promo_target", cid_)
                set_setting("promo_mode", 1)
                show(chat_id, mid, ("🎯 Включить задание\n\nПо ссылке канал определить не удалось "
                                    "(возможно, он приватный). Перешлите сюда любой пост из этого канала — "
                                    "и бот включит задание.\n\nБот должен быть админом канала.",
                                    markup([cb("Отмена", "pr:cancel")])))
            return
        if act == "t":
            db.execute("UPDATE promo_channels SET active=1-active WHERE id=?", (int(parts[2]),))
            db.commit()
            show(chat_id, mid, screen_promo_item(int(parts[2])))
            return
        if act == "n":
            db.execute("UPDATE promo_channels SET need=? WHERE id=?", (int(parts[3]), int(parts[2])))
            db.commit()
            show(chat_id, mid, screen_promo_item(int(parts[2])))
            return
        if act == "d":
            cid_ = int(parts[2])
            for t_ in ("c_links", "c_joins", "c_rewards"):
                db.execute(f"DELETE FROM {t_} WHERE camp_id=?", (cid_,))
            db.execute("DELETE FROM promo_channels WHERE id=?", (cid_,))
            db.commit()
        elif act in ("menu", "gift"):
            key = "promo_" + act
            set_setting(key, "0" if promo_on(key) else "1")
        elif act == "add":
            set_setting("promo_mode", 1)
            set_setting("promo_target", "")
            set_setting("add_mode", 0)
            show(chat_id, mid, screen_promo_add())
            return
        elif act == "cancel":
            set_setting("promo_mode", 0)
            set_setting("promo_target", "")
        show(chat_id, mid, screen_promo_admin())
    elif uid == ADMIN_ID and data.startswith("rv_ok:"):
        rid = int(data.split(":")[1])
        ok = publish_review(rid)
        try:
            api("editMessageReplyMarkup", chat_id=chat_id, message_id=mid, reply_markup={"inline_keyboard": []})
        except Exception:
            pass
        send(uid, "✅ Опубликовано" if ok else "⚠️ Не удалось опубликовать (уже обработан или ошибка)")
    elif uid == ADMIN_ID and data.startswith("rv_no:"):
        rid = int(data.split(":")[1])
        db.execute("UPDATE reviews SET status='rejected' WHERE id=? AND status='pending'", (rid,))
        db.commit()
        try:
            api("editMessageReplyMarkup", chat_id=chat_id, message_id=mid, reply_markup={"inline_keyboard": []})
        except Exception:
            pass
        send(uid, "❌ Отклонено")


def handle_update(upd):
    if "channel_post" in upd:
        handle_channel_post(upd["channel_post"])
    elif "chat_member" in upd:
        if upd["chat_member"]["chat"]["id"] == CHANNEL_ID:
            handle_chat_member(upd["chat_member"])
        else:
            handle_camp_member(upd["chat_member"])
    elif "callback_query" in upd:
        handle_callback(upd["callback_query"])
    elif "message" in upd:
        handle_message(upd["message"])


def main():
    load_emoji()
    try:
        migrate_promos()
    except Exception as e:
        print("migrate error:", e)
    backup_db(force=True)
    print("Bot started", BOT_VERSION, "| DB:", DB_PATH)
    offset = None
    while True:
        try:
            daily_check()
            backup_db()
            params = {"timeout": 30,
                      "allowed_updates": ["message", "callback_query", "chat_member", "channel_post"]}
            if offset is not None:
                params["offset"] = offset
            for upd in api("getUpdates", **params):
                offset = upd["update_id"] + 1
                try:
                    handle_update(upd)
                except Exception as e:
                    print("update error:", e)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("loop error:", e)
            time.sleep(3)


if __name__ == "__main__":
    main()
