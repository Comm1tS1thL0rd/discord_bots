### the bot has been made by @Comm1tS1thL0rd (git) and remians as his property, any use of this code must be credited to him and him only.
### This bot verifies students based on their student ID and assigns roles accordingly.

import discord
from discord.ext import commands
import re
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

BRANCH_CODES = {   ### Change if we do add more campuses or branches
    
    'A1': 'Chem.',          # Chemical Engineering
    'A3': 'EEE',            # Electrical and Electronics Engineering
    'A4': 'Mech.',          # Mechanical Engineering
    'A7': 'CSE',            # Computer Science Engineering
    'A8': 'ENI',            # Electronics and Instrumentation Engineering   
    'AA': 'ECE',            # Electronics and Communication Engineering
    'AC': 'EnC',            # Electronics and Computer Engineering
    'AD': 'MnC',            # Mathematics and Computing
    'AJ': 'ESE',            # Environmental and Sustainability Engineering
    'B1': 'Msc Bio.',       # M.Sc. Biological Sciences
    'B2': 'Msc Chem.',      # M.Sc. Chemistry
    'B3': 'Msc Eco.',       # M.Sc. Economics
    'B4': 'Msc Math',       # M.Sc. Mathematics
    'B5': 'Msc Phy.',       # M.Sc. Physics
    'B7': 'Msc Semi.'       # M.Sc. Semiconductor and Nanoscience
}

CITY_CODES = {   ### leaving it here if in case we expand to more campuses
    'G': 'Goa',
}

def parse_student_id(student_id):
    pattern = r'^(\d{4})([A-Z]{1,2}\d?)([A-Z]{1,2}\d?|PS|TS|IS|UB|RM)(\d{4})([A-Z])$'
    match = re.match(pattern, student_id.upper())
    
    if match:
        batch = match.group(1)
        first_branch_code = match.group(2)
        middle_code = match.group(3)
        roll_number = match.group(4)
        city_code = match.group(5)
        
        if middle_code in ['PS', 'TS', 'IS', 'UB', 'RM']:
            second_branch_code = None
            second_branch_name = None
        else:
            second_branch_code = middle_code
            second_branch_name = BRANCH_CODES.get(second_branch_code, 'Unknown Branch')
        
        return {
            'batch': batch,
            'first_branch_code': first_branch_code,
            'first_branch_name': BRANCH_CODES.get(first_branch_code, 'Unknown Branch'),
            'second_branch_code': second_branch_code,
            'second_branch_name': second_branch_name,
            'roll_number': roll_number,
            'city_code': city_code,
            'city_name': CITY_CODES.get(city_code, 'Unknown Campus'),
            'valid': True,
            'has_dual_branch': second_branch_code is not None
        }
    return {'valid': False}

async def create_role_if_not_exists(guild, role_name, color=discord.Color.default()):
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        try:
            role = await guild.create_role(name=role_name, color=color)
        except discord.Forbidden:
            return None
    return role

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')

@bot.event
async def on_message(message):

    ALLOWED_CHANNEL_ID = 1384090905794969620 
    
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return    
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

async def remove_old_roles_roles(member):
    batch_keywords = ["Batch"]
    branch_names = list(BRANCH_CODES.values())
    campus_keywords = ["Campus"]
    special_roles = ["Alumni"]
    
    roles_to_remove = []
    
    for role in member.roles:
        if any(keyword in role.name for keyword in batch_keywords):
            roles_to_remove.append(role)
        elif role.name in branch_names:
            roles_to_remove.append(role)
        elif any(keyword in role.name for keyword in campus_keywords):
            roles_to_remove.append(role)
        elif role.name in special_roles:
            roles_to_remove.append(role)
    
    if roles_to_remove:
        await member.remove_roles(*roles_to_remove, reason="Removing old roles roles before re-roles")

@bot.command(name='verify')
async def verify_user(ctx, student_id: str = None):
    if not student_id:
        embed = discord.Embed(
            title="❌ Invalid Format",
            description="Please provide your student ID.\n\n**Examples:**\n`!verify 2025A4PS0123P` (Single branch)\n`!verify 2025A4A70123P` (Dual branch)",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    parsed_data = parse_student_id(student_id)
    
    if not parsed_data['valid']:
        embed = discord.Embed(
            title="❌ Invalid Student ID",
            description="Please check your ID format and try again.\n\n**Expected format:** `YYYYXXYYNNNNC`\n- YYYY: Year (e.g., 2025)\n- XX: First branch code (e.g., A4)\n- YY: PS/TS or second branch code (e.g., A7)\n- NNNN: Roll number\n- C: Campus code (only supports Goa now)",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    if parsed_data['city_name'] == 'Unknown Campus':
        embed = discord.Embed(
            title="🚫 Campus Not Supported",
            description="This is an exclusive Bits Pilani Goa Campus server, try joining the BITS Pilani Discord server if you are from any other campus or institution",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    batch_year = int(parsed_data['batch'])
    
    if batch_year > 2025:
        embed = discord.Embed(
            title="❌ Invalid Batch Year",
            description=f"**Batch year {batch_year} is not allowed.**\n\nOnly students from **2025 and earlier** can verify.\n\nIf this is an error, please contact an administrator.",
            color=discord.Color.red()
        )
        embed.add_field(name="Allowed Range", value="Up to 2025 batch", inline=True)
        embed.add_field(name="Your Batch", value=f"{batch_year} (Not allowed)", inline=True)
        await ctx.send(embed=embed)
        return
    
    guild = ctx.guild
    member = ctx.author
    
    await remove_old_roles_roles(member)
    
    if batch_year < 2021:
        batch_role_name = "Alumni"
        batch_description = f"Alumni (Class of {batch_year})"
        is_alumni = True
    else:
        batch_role_name = f"{parsed_data['batch']} Batch"
        batch_description = f"{parsed_data['batch']} Batch"
        is_alumni = False
    
    campus_role_name = f"{parsed_data['city_name']} Campus"
    
    roles_to_assign = []
    missing_roles = []
    
    batch_role = discord.utils.get(guild.roles, name=batch_role_name)
    if batch_role:
        roles_to_assign.append(batch_role)
    else:
        missing_roles.append(batch_role_name)
    
    if not is_alumni:
        first_branch_role = discord.utils.get(guild.roles, name=parsed_data['first_branch_name'])
        if first_branch_role:
            roles_to_assign.append(first_branch_role)
        else:
            missing_roles.append(parsed_data['first_branch_name'])
        
        if parsed_data['has_dual_branch'] and parsed_data['second_branch_name']:
            second_branch_role = discord.utils.get(guild.roles, name=parsed_data['second_branch_name'])
            if second_branch_role:
                roles_to_assign.append(second_branch_role)
            else:
                missing_roles.append(parsed_data['second_branch_name'])
    
    campus_role = discord.utils.get(guild.roles, name=campus_role_name)
    if campus_role:
        roles_to_assign.append(campus_role)
    else:
        missing_roles.append(campus_role_name)
    
    if missing_roles:
        embed = discord.Embed(
            title="❌ Required Roles Not Found",
            description="Some required roles are missing from the server. Please contact an administrator.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Missing Roles",
            value="\n".join([f"• {role}" for role in missing_roles]),
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    try:
        await member.add_roles(*roles_to_assign, reason="Student roles")
        
        if is_alumni:
            embed = discord.Embed(
                title="🎓 Alumni Role Assigned!",
                description=f"Welcome back, {member.mention}!",
                color=discord.Color.purple()
            )
            embed.add_field(name="Status", value="Alumni", inline=True)
            embed.add_field(name="Batch Year", value=parsed_data['batch'], inline=True)
        else:
            embed = discord.Embed(
                title="✅ Roles Assigned!",
                description=f"Welcome, {member.mention}!",
                color=discord.Color.green()
            )
            embed.add_field(name="Batch", value=parsed_data['batch'], inline=True)
        
        if not is_alumni:
            embed.add_field(name="Primary Branch", value=parsed_data['first_branch_name'], inline=True)
            
            if parsed_data['has_dual_branch']:
                embed.add_field(name="Secondary Branch", value=parsed_data['second_branch_name'], inline=True)
        
        embed.add_field(name="Campus", value=parsed_data['city_name'], inline=True)
        embed.add_field(
            name="Assigned Roles", 
            value="\n".join([f"• {role.name}" for role in roles_to_assign]),
            inline=False
        )
        
        if not is_alumni and parsed_data['has_dual_branch']:
            embed.add_field(
                name="🎓 Dual Branch Detected!", 
                value="You've been assigned roles for both branches!",
                inline=False
            )
        
        if is_alumni:
            embed.add_field(
                name="🏆 Alumni Status", 
                value="You've been assigned Alumni role for graduating before 2021!",
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to assign roles. Please contact an admin.")

@bot.command(name='info')
async def user_info(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    
    embed = discord.Embed(
        title=f"User Info: {member.display_name}",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Roles", 
        value="\n".join([role.name for role in member.roles[1:]]) or "No roles",
        inline=False
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='test_parse')
async def test_parse(ctx, student_id: str):
    parsed = parse_student_id(student_id)
    
    if parsed['valid']:
        embed = discord.Embed(title="✅ Parsing Test Results", color=discord.Color.green())
        embed.add_field(name="Batch", value=parsed['batch'], inline=True)
        embed.add_field(name="First Branch", value=f"{parsed['first_branch_code']} - {parsed['first_branch_name']}", inline=True)
        
        if parsed['has_dual_branch']:
            embed.add_field(name="Second Branch", value=f"{parsed['second_branch_code']} - {parsed['second_branch_name']}", inline=True)
        else:
            embed.add_field(name="Second Branch", value="None (PS/TS/IS/UB/RM)", inline=True)
            
        embed.add_field(name="Campus", value=f"{parsed['city_code']} - {parsed['city_name']}", inline=True)
        embed.add_field(name="Roll Number", value=parsed['roll_number'], inline=True)
        embed.add_field(name="Dual Branch?", value="Yes" if parsed['has_dual_branch'] else "No", inline=True)
    else:
        embed = discord.Embed(title="❌ Invalid ID Format", color=discord.Color.red())
        embed.add_field(name="Expected Format", value="YYYYXXYYNNNNC", inline=False)
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("DISCORD_BOT_TOKEN not found!")
    else:
        print("🤖 Starting bot...")
        bot.run(TOKEN)