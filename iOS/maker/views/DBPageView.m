//
//  DBPageView.m
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import "DBPageView.h"
#import "DBActionView.h"
#import "DBEnv.h"
#import <SDWebImage/UIImageView+WebCache.h>

@implementation DBPageView

- (id)initWithFrame:(CGRect)frame andPage:(DBPage *)page referId:(NSString *)refer touchHandler:(id<DBTouchControl>)delegate
{
    self = [super initWithFrame:frame];
    if (self) {
        NSLog(@"page rect: %f, %f, %f, %f",
              page.rect.origin.x, page.rect.origin.y, page.rect.size.width, page.rect.size.height);
        if ([page.type isEqualToString:PAGE_TYPE_DIALOG]){
            self.backgroundColor = [UIColor clearColor];
        }else{
            self.backgroundColor = [[UIColor alloc] initWithRed:0.0 green:0.0 blue:1.0 alpha:0.3];
        }
        //[self setBackgroundColor:[UIColor redColor]];
        
        NSLog(@"set page");
        
        if (page.photo.length > 0){
            self.box = [[UIImageView alloc] initWithFrame:self.frame];
            UIImageView * iv = (UIImageView *)self.box;
            [iv setImageWithURL:[[NSURL alloc] initWithString:page.photo]];
        }else{
            self.box = [[UIView alloc] initWithFrame:self.frame];
            [self.box setBackgroundColor:[[UIColor alloc] initWithRed:0.0 green:1.0 blue:1.0 alpha:0.3]];
        }
        [self addSubview:self.box];
        
        for (int i = 0; i < page.actions.count; i++){
            DBAction * a = page.actions[i];
            NSLog(@"add action, %@, %d", a.type, i);
            
            if ([a.type isEqualToString:ACTION_TYPE_INPUT]){
                UITextField * v = [[UITextField alloc] initWithFrame:a.rect];
                v.text = @"Input something...";
                if ([page.type isEqualToString:PAGE_TYPE_DIALOG]){
                    [v setFrame:CGRectMake(a.rect.origin.x + page.rect.origin.x,
                                           a.rect.origin.y + page.rect.origin.y,
                                           a.rect.size.width, a.rect.size.height)];
                }

                [self addSubview:v];
                continue;
            }
            
            DBActionView * v = [[DBActionView alloc] initWithFrame:a.rect pageId:page.id referId:refer action:a];
            [v setBackgroundColor:[[UIColor alloc] initWithRed:1.0 green:0.0 blue:0.0 alpha:0.1]];
            NSLog(@"action rect: %f, %f, %f, %f",
                  a.rect.origin.x, a.rect.origin.y, a.rect.size.width, a.rect.size.height);
            //[v setBackgroundColor:[[UIColor alloc] initWithRed:1.0 green:1.0 blue:0.0 alpha:1.0]];
            NSLog(@"v %f %f", v.frame.origin.x, v.frame.size.width);
            
            if ([page.type isEqualToString:PAGE_TYPE_DIALOG]){
                [v setFrame:CGRectMake(a.rect.origin.x + page.rect.origin.x,
                                      a.rect.origin.y + page.rect.origin.y,
                                      a.rect.size.width, a.rect.size.height)];
            }
            [self addSubview:v];
            
            if ([a.type isEqualToString:ACTION_TYPE_TOUCH] || [a.type isEqualToString:ACTION_TYPE_BACK]){
            
                UITapGestureRecognizer * tg = [[UITapGestureRecognizer alloc]
                                                    initWithTarget:delegate action:@selector(onTap:)];
                [v addGestureRecognizer:tg];
            }else{
                NSRange r =[ACTION_TYPE_SLIDE rangeOfString:a.type options:NSCaseInsensitiveSearch];
                if (r.length > 0){
                    UISwipeGestureRecognizer * sg = [[UISwipeGestureRecognizer alloc]
                                                     initWithTarget:delegate action:@selector(onSlide:)];
                    if ([a.type isEqualToString:ACTION_TYPE_SLIDE_LEFT]){
                        sg.direction = UISwipeGestureRecognizerDirectionLeft;
                    }else if([a.type isEqualToString:ACTION_TYPE_SLIDE_RIGHT]){
                        sg.direction = UISwipeGestureRecognizerDirectionRight;
                    }else if([a.type isEqualToString:ACTION_TYPE_SLIDE_UP]){
                        sg.direction = UISwipeGestureRecognizerDirectionUp;
                    }else if([a.type isEqualToString:ACTION_TYPE_SLIDE_DOWN]){
                        sg.direction = UISwipeGestureRecognizerDirectionDown;
                    }
                    [v addGestureRecognizer:sg];
                }
            }

        }
        
    }
    return self;
    
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{
    // Drawing code
}
*/

@end
