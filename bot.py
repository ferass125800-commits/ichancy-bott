import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7838955950
MIN_DEPOSIT = 5000  # الحد الأدنى للشحن بالليرة السورية

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
user_accounts = {}
user_states = {}

def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton("🔴 دخول منصة Ichancy", url="https://www.ichancy300.com/ar"))
    keyboard.add(
        types.InlineKeyboardButton("⚡ شحن رصيد البوت", callback_data="btn_deposit"),
        types.InlineKeyboardButton("💰 سحب رصيد البوت", callback_data="btn_withdraw")
    )
    keyboard.add(
        types.InlineKeyboardButton("👤 إنشاء حساب جديد", callback_data="btn_create_acc"),
        types.InlineKeyboardButton("ℹ️ معلومات حسابي", callback_data="btn_ichancy_info")
    )
    keyboard.add(
        types.InlineKeyboardButton("📝 رسالة للإدارة", callback_data="btn_msg_admin"),
        types.InlineKeyboardButton("💌 تواصل معنا", callback_data="btn_contact")
    )
    keyboard.add(
        types.InlineKeyboardButton("↗️ تحميل تطبيق Ichancy APK", url="https://android.betcoapps.com/novichok/ichancy_com/ichancy_com.apk")
    )
    keyboard.add(
        types.InlineKeyboardButton("🎰 الجاكبوت والعروض", callback_data="btn_offers")
    )
    return keyboard

def get_main_menu_button():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🟩 القائمة الرئيسية", callback_data="go_main"))
    return kb

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_id = message.from_user.id
    acc = user_accounts.get(user_id)
    
    if acc:
        text = (
            f"<b>أهلاً بك مجدداً في بوت Ichancy Swaida 🚀</b>\n\n"
            f"🌐 <b>رابط الموقع المباشر:</b> <a href='https://www.ichancy300.com/ar'>ichancy300.com</a>\n\n"
            f"👤 <b>اسم الحساب:</b> <code>{acc['username']}</code>\n"
            f"🔑 <b>كلمة السر:</b> <code>{acc['password']}</code>\n"
            f"💰 <b>الرصيد:</b> {acc['balance']} ل.س"
        )
    else:
        text = (
            f"<b>أهلاً بك في بوت Ichancy Swaida الرسمي 🎲</b>\n\n"
            f"يمكنك إنشاء حسابك على موقع Ichancy المباشر وشحن وسحب رصيدك بكل سهولة.\n\n"
            f"🌐 <b>رابط المنصة:</b> <a href='https://www.ichancy300.com/ar'>https://www.ichancy300.com/ar</a>\n\n"
            f"اضغط على <b>'👤 إنشاء حساب جديد'</b> للبدء."
        )
    bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: True)
def process_callbacks(call):
    code = call.data
    user_id = call.from_user.id
    acc = user_accounts.get(user_id)

    if code == "go_main":
        user_states.pop(user_id, None)
        bot.edit_message_text("<b>أهلاً بك في بوت Ichancy Swaida</b>", call.message.chat.id, call.message.message_id, reply_markup=get_main_keyboard())

    elif code == "btn_create_acc":
        user_states[user_id] = "waiting_username"
        bot.edit_message_text(
            "<b>👤 إنشاء حساب جديد على Ichancy:</b>\n\nالرجاء إدخال <b>اسم المستخدم (Username)</b> الذي ترغب به باللغة الإنجليزية (مثال: <code>Player99</code>):",
            call.message.chat.id, call.message.message_id, reply_markup=get_main_menu_button()
        )

    elif code == "btn_ichancy_info":
        if acc:
            info_text = (
                f"<b>بيانات حسابك في Ichancy Swaida:</b>\n\n"
                f"👤 <b>اسم المستخدم:</b> <code>{acc['username']}</code>\n"
                f"🔑 <b>كلمة السر:</b> <code>{acc['password']}</code>\n"
                f"💰 <b>الرصيد المتاح:</b> {acc['balance']} ل.س"
            )
        else:
            info_text = "⚠️ ليس لديك حساب مسجل بعد. اضغط على 'إنشاء حساب جديد'."
        bot.edit_message_text(info_text, call.message.chat.id, call.message.message_id, reply_markup=get_main_menu_button())

    elif code == "btn_deposit":
        if not acc:
            bot.answer_callback_query(call.id, "⚠️ يجب عليك إنشاء حساب أولاً قبل الشحن!", show_alert=True)
            return

        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton("🟢 Syriatel Cash 🟢", callback_data="dep_syriatel"),
            types.InlineKeyboardButton("⚡ Sham Cash Auto ⚡", callback_data="dep_sham"),
            types.InlineKeyboardButton("🟩 القائمة الرئيسية", callback_data="go_main")
        )
        bot.edit_message_text("<b>اختر طريقة الشحن المناسبة:</b>", call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif code == "dep_syriatel":
        user_states[user_id] = "waiting_deposit_amount"
        bot.edit_message_text(
            f"<b>🟢 الشحن عبر سيرياتيل كاش</b>\n\n"
            f"أدخل المبلغ المراد شحنه بالأرقام فقط (مثال: <code>100000</code>)\n"
            f"⚠️ <i>الحد الأدنى للشحن هو {MIN_DEPOSIT:,} ل.س:</i>",
            call.message.chat.id, call.message.message_id, reply_markup=get_main_menu_button()
        )

    elif code == "btn_withdraw":
        if not acc:
            bot.answer_callback_query(call.id, "⚠️ ليس لديك حساب مسجل بعد!", show_alert=True)
            return

        user_states[user_id] = "waiting_withdraw_request"
        bot.edit_message_text(
            "<b>💰 سحب الرصيد</b>\n\nالرجاء إرسال المبلغ ورقم المحفظة لاستلام الأرباح:",
            call.message.chat.id, call.message.message_id, reply_markup=get_main_menu_button()
        )

    elif code.startswith("approve_dep_"):
        parts = code.split("_")
        target_user_id = int(parts[2])
        amount = parts[3]
        
        bot.answer_callback_query(call.id, "تم قبول الشحن!")
        bot.edit_message_text(call.message.text + f"\n\n<b>[✅ تم قبول الشحن وإضافة {amount} ل.س]</b>", call.message.chat.id, call.message.message_id)
        
        if target_user_id in user_accounts:
            user_accounts[target_user_id]['balance'] += float(amount)

        try:
            bot.send_message(target_user_id, f"🎉 <b>تم قبول طلب الشحن الخاص بك بنجاح!\nتم إضافة {int(amount):,} ل.س إلى حسابك.</b>")
        except:
            pass

    elif code.startswith("reject_dep_"):
        target_user_id = int(code.split("_")[2])
        bot.answer_callback_query(call.id, "تم رفض الطلب")
        bot.edit_message_text(call.message.text + "\n\n<b>[❌ تم رفض طلب الشحن]</b>", call.message.chat.id, call.message.message_id)
        try:
            bot.send_message(target_user_id, "⚠️ <b>عذراً، تم رفض طلب الشحن. يرجى مراجعة الإدارة والتأكد من عملية التحويل.</b>")
        except:
            pass

    else:
        bot.answer_callback_query(call.id, "هذا الزر قيد التطوير أو غير مفعل حالياً", show_alert=True)

@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_user_inputs(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    text = message.text.strip()

    if state == "waiting_username":
        user_states[user_id] = f"waiting_password_{text}"
        bot.reply_to(message, f"تم اختيار اسم المستخدم: <code>{text}</code>\n\nالآن أدخل <b>كلمة السر</b> التي ترغب بها للحساب:")

    elif state and state.startswith("waiting_password_"):
        chosen_username = state.split("_")[2]
        chosen_password = text
        user_states.pop(user_id, None)

        user_accounts[user_id] = {
            "username": chosen_username,
            "password": chosen_password,
            "balance": 0.0
        }

        bot.reply_to(
            message,
            f"✅ <b>تم استلام طلب إنشاء الحساب بنجاح!</b>\n\n"
            f"👤 <b>اسم المستخدم:</b> <code>{chosen_username}</code>\n"
            f"🔑 <b>كلمة السر:</b> <code>{chosen_password}</code>\n\n"
            f"سيتم تفعيل الحساب على موقع Ichancy فوراً من قبل الإدارة.",
            reply_markup=get_main_keyboard()
        )

        admin_msg = (
            f"🆕 <b>طلب إنشاء حساب جديد على Ichancy!</b>\n\n"
            f"🆔 <b>مُعرف التليجرام:</b> <code>{user_id}</code>\n"
            f"👤 <b>اسم المستخدم المطلوب:</b> <code>{chosen_username}</code>\n"
            f"🔑 <b>كلمة السر المطلوبة:</b> <code>{chosen_password}</code>"
        )
        bot.send_message(ADMIN_ID, admin_msg)

    elif state == "waiting_deposit_amount":
        # تحقق صارم من أن المبلغ أرقام فقط
        if not text.isdigit():
            bot.reply_to(message, "❌ <b>عذراً، يجب كتابة المبلغ بالأرقام فقط (مثال: 50000) دون أي أحرف أو رموز!</b>")
            return
        
        amount = int(text)
        if amount < MIN_DEPOSIT:
            bot.reply_to(message, f"❌ <b>المبلغ أدنى من الحد المسموح!</b>\nالحد الأدنى للشحن هو <b>{MIN_DEPOSIT:,} ل.س</b>. يرجى إدخال مبلغ أكبر:")
            return

        user_states[user_id] = f"waiting_dep_proof_{amount}"
        bot.reply_to(message, f"تم تسجيل المبلغ المطلوب: <b>{amount:,} ل.س</b>.\n\nالآن يرجى إرسال <b>رقم عملية التحويل (رقم المعاملة بالأرقام فقط):</b>")

    elif state and state.startswith("waiting_dep_proof_"):
        # تحقق صارم من أن رقم المعاملة أرقام فقط ولا يقل عن 6 أرقام
        if not text.isdigit() or len(text) < 6:
            bot.reply_to(message, "❌ <b>رقم المعاملة غير صحيح!</b>\nيرجى إدخال <b>رقم العملية/المعاملة بالأرقام فقط</b> (مثال: <code>64839201</code>):")
            return

        amount = state.split("_")[3]
        user_states.pop(user_id, None)
        bot.reply_to(message, "⏳ <b>تم إرسال طلب الشحن للإدارة بنجاح!</b>\nسيتم مراجعة التحويل وشحن حسابك فور التأكد.")
        
        acc = user_accounts.get(user_id, {"username": "غير معروف"})
        admin_msg = (
            f"🚨 <b>طلب شحن جديد!</b>\n\n"
            f"👤 <b>الحساب:</b> <code>{acc['username']}</code>\n"
            f"💵 <b>المبلغ المطلوب:</b> {int(amount):,} ل.س\n"
            f"📄 <b>رقم المعاملة:</b> <code>{text}</code>"
        )
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(
            types.InlineKeyboardButton("✅ قبول الشحن", callback_data=f"approve_dep_{user_id}_{amount}"),
            types.InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_dep_{user_id}")
        )
        bot.send_message(ADMIN_ID, admin_msg, reply_markup=kb)

    elif state == "waiting_withdraw_request":
        user_states.pop(user_id, None)
        bot.reply_to(message, "⏳ <b>تم إرسال طلب السحب للإدارة بنجاح!</b>")
        admin_msg = f"🚨 <b>طلب سحب جديد!</b>\n\n📝 <b>التفاصيل:</b> {text}"
        bot.send_message(ADMIN_ID, admin_msg)

if __name__ == '__main__':
    print("Ichancy Swaida Bot with Strict Number & Deposit Validation is running...")
    bot.infinity_polling()
